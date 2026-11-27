// Marketix: purge the WP-Optimize page cache when the site is edited (WPCode, PHP Snippet, Run Everywhere)
// Page/post edits clear only the pages they appear on. Site-wide changes (templates, header/footer, site settings,
// custom code, menus, Customizer, categories, Elementor CSS regeneration) clear everything. A full purge makes
// WP-Optimize rebuild every page, which loads the server for a minute, so it is kept for changes that need it.
function mx_full_purge() {
	static $queued = false;
	if ( $queued ) {
		return;
	}
	$queued = true;
	add_action( 'shutdown', 'mx_run_full_purge', 1 );
}

function mx_run_full_purge() {
	if ( function_exists( 'wpo_cache_flush' ) ) {
		wpo_cache_flush();
	}
}

function mx_purge_one( $post_id ) {
	if ( ! class_exists( 'WPO_Page_Cache' ) ) {
		return;
	}
	WPO_Page_Cache::delete_single_post_cache( $post_id );
	WPO_Page_Cache::delete_homepage_cache();
	if ( 'post' === get_post_type( $post_id ) ) {
		WPO_Page_Cache::delete_cache_by_url( home_url( '/insights/' ), false );
		foreach ( wp_get_post_categories( $post_id ) as $cat_id ) {
			WPO_Page_Cache::delete_cache_by_url( get_category_link( $cat_id ), true );
		}
	}
}

function mx_purge_for_post( $post_id ) {
	$type = get_post_type( $post_id );
	if ( 'page' === $type || 'post' === $type ) {
		mx_purge_one( $post_id );
	} elseif ( in_array( $type, array( 'elementor_library', 'elementor_snippet', 'wpcode', 'nav_menu_item' ), true ) ) {
		mx_full_purge();
	}
}

function mx_purge_on_status( $new_status, $old_status, $post ) {
	if ( 'publish' !== $new_status && 'publish' !== $old_status ) {
		return;
	}
	if ( wp_is_post_revision( $post ) || wp_is_post_autosave( $post ) ) {
		return;
	}
	mx_purge_for_post( $post->ID );
}
add_action( 'transition_post_status', 'mx_purge_on_status', 10, 3 );

function mx_purge_after_elementor_save( $post_id ) {
	if ( 'publish' === get_post_status( $post_id ) ) {
		mx_purge_for_post( $post_id );
	}
}
add_action( 'elementor/editor/after_save', 'mx_purge_after_elementor_save' );

add_action( 'before_delete_post', 'mx_purge_for_post' );
add_action( 'elementor/core/files/clear_cache', 'mx_full_purge' );
add_action( 'wp_update_nav_menu', 'mx_full_purge' );
add_action( 'customize_save_after', 'mx_full_purge' );
add_action( 'created_term', 'mx_full_purge' );
add_action( 'edited_term', 'mx_full_purge' );
add_action( 'delete_term', 'mx_full_purge' );
