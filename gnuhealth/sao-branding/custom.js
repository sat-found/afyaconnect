/* AfyaConnect branding and UX enhancements for Tryton SAO */
(function() {
    'use strict';

    if (typeof Sao === 'undefined') {
        return;
    }

    Sao.config.title = 'AfyaConnect';
    Sao.config.bug_url = 'https://github.com/sat-found/afyaconnect/issues';
    Sao.config.icon_colors = '#0d9488,#1e293b,#f59e0b'.split(',');
    Sao.config.graph_color = '#0d9488';
    Sao.config.calendar_colors = '#ffffff,#0d9488'.split(',');

    var logoSvg = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48" fill="none">'
        + '<rect width="48" height="48" rx="12" fill="white" fill-opacity="0.2"/>'
        + '<path d="M24 10c-6.6 0-12 5.4-12 12 0 8.4 12 16 12 16s12-7.6 12-16c0-6.6-5.4-12-12-12z"'
        + ' fill="white"/>'
        + '<circle cx="24" cy="22" r="5" fill="#0d9488"/>'
        + '<path d="M14 34h20" stroke="white" stroke-width="2.5" stroke-linecap="round"/>'
        + '</svg>';

    var originalLoginDialog = Sao.Session.login_dialog;
    Sao.Session.login_dialog = function() {
        var dialog = originalLoginDialog();
        dialog.modal.addClass('afya-login-modal');

        var hero = jQuery('<div/>', {'class': 'afya-login-hero'});
        hero.append(
            jQuery('<div/>', {'class': 'afya-login-logo'}).html(logoSvg),
            jQuery('<h2/>', {'class': 'afya-login-title'}).text('AfyaConnect'),
            jQuery('<p/>', {'class': 'afya-login-tagline'}).text(
                'GNU Health · AI-assisted triage · Citizen access')
        );

        var formWrap = jQuery('<div/>', {'class': 'afya-login-form'});
        dialog.body.children().appendTo(formWrap);

        dialog.body.empty().append(hero, formWrap);
        dialog.body.append(
            jQuery('<p/>', {'class': 'afya-login-hint'}).text(
                'Local dev: database health · user admin')
        );

        jQuery.when(Sao.DB.list()).then(function(databases) {
            if (databases && databases.indexOf('health') >= 0) {
                dialog.database_select.val('health');
                dialog.database_input.val('health');
            }
        });

        return dialog;
    };

    jQuery(function() {
        document.title = 'AfyaConnect';
        jQuery('html').attr('theme', 'afyaconnect');
        jQuery('.body').addClass('afya-app-ready');
    });
}());
