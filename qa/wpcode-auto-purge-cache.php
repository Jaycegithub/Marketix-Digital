/**
 * Marketix – purge the WP-Optimize page cache automatically (WPCode → PHP Snippet → Run Everywhere).
 *
 * WP-Optimize only purges the single post you edit. Edits to templates, the header/footer, menus, Elementor site settings
 * or an Elementor CSS cache clear change every page, so the whole cache is purged instead. The purge runs once at the end
 * of the request, however many items were saved. Cloudflare serves HTML uncached (cf-cache-status: DYNAMIC), so it
 * needs no purge here.
 */
function mx_queue_cache_purge() {
	if ( ! empty( $GLOBALS['mx_purge_queued'] ) ) {
		return;
	}
	$GLOBALS['mx_purge_queued'] = true;
	add_action( 'shutdown', 'mx_run_cache_purge', 1 );
}

function mx_run_cache_purge() {
	if ( function_exists( 'wpo_cache_flush' ) ) {
		wpo_cache_flush();
	} elseif ( function_exists( 'WP_Optimize' ) && is_callable( array( WP_Optimize()->get_page_cache(), 'purge' ) ) ) {
		WP_Optimize()->get_page_cache()->purge();
	}
}

// Pages, posts, Elementor templates / site settings / custom code: when something is published, updated or unpublished.
add_action( 'transition_post_status', function ( $new_status, $old_status, $post ) {
	if ( 'publish' !== $new_status && 'publish' !== $old_status ) {
		return; // drafts and autosaves don't change the live site
	}
	if ( wp_is_post_revision( $post ) || wp_is_post_autosave( $post ) ) {
		return;
	}
	$types = array( 'page', 'post', 'elementor_library', 'elementor_snippet', 'wpcode', 'nav_menu_item' );
	if ( in_array( $post->post_type, $types, true ) ) {
		mx_queue_cache_purge();
	}
}, 10, 3 );

add_action( 'deleted_post', 'mx_queue_cache_purge' );               // a page or post deleted permanently
add_action( 'elementor/editor/after_save', 'mx_queue_cache_purge' ); // Elementor "Update" (pages, templates, site settings)
add_action( 'elementor/core/files/clear_cache', 'mx_queue_cache_purge' ); // Elementor → Tools → Regenerate CSS & Data
add_action( 'wp_update_nav_menu', 'mx_queue_cache_purge' );         // menus
add_action( 'customize_save_after', 'mx_queue_cache_purge' );       // Customizer (site icon, logo…)
add_action( 'created_term', 'mx_queue_cache_purge' );               // categories / tags
add_action( 'edited_term', 'mx_queue_cache_purge' );
add_action( 'delete_term', 'mx_queue_cache_purge' );
