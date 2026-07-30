<?php
WP_CLI::add_wp_hook( 'pre_option_WPLANG', function() {
    return 'en_US';
});
