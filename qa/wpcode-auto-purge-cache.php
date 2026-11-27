// Marketix: purge the WP-Optimize page cache when the site is edited (WPCode, PHP Snippet, Run Everywhere)
function mx_queue_cache_purge() {
	static $queued = false;
	if ( $queued ) {
		return;
	}
	$queued = true;
	add_action( 'shutdown', 'mx_run_cache_purge', 1 );
}

function mx_run_cache_purge() {
	if ( function_exists( 'wpo_cache_flush' ) ) {
		wpo_cache_flush();
	}
}

function mx_purge_on_status( $new_status, $old_status, $post ) {
	if ( 'publish' !== $new_status && 'publish' !== $old_status ) {
		return;
	}
	if ( wp_is_post_revision( $post ) || wp_is_post_autosave( $post ) ) {
		return;
	}
	$types = array( 'page', 'post', 'elementor_library', 'elementor_snippet', 'wpcode', 'nav_menu_item' );
	if ( in_array( $post->post_type, $types, true ) ) {
		mx_queue_cache_purge();
	}
}
add_action( 'transition_post_status', 'mx_purge_on_status', 10, 3 );

add_action( 'deleted_post', 'mx_queue_cache_purge' );
add_action( 'elementor/editor/after_save', 'mx_queue_cache_purge' );
add_action( 'elementor/core/files/clear_cache', 'mx_queue_cache_purge' );
add_action( 'wp_update_nav_menu', 'mx_queue_cache_purge' );
add_action( 'customize_save_after', 'mx_queue_cache_purge' );
add_action( 'created_term', 'mx_queue_cache_purge' );
add_action( 'edited_term', 'mx_queue_cache_purge' );
add_action( 'delete_term', 'mx_queue_cache_purge' );
