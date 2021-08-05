from flaskr.blog import blog

blog.blog_bp.add_url_rule('/', view_func=blog.home, methods=('GET',))
blog.blog_bp.add_url_rule('/contact/', view_func=blog.contact, methods=('GET', 'POST',))
blog.blog_bp.add_url_rule('/search/', view_func=blog.search_post, methods=('GET',))
blog.blog_bp.add_url_rule('/author/', view_func=blog.author_details, methods=('GET',))  # GET param - author_id
blog.blog_bp.add_url_rule('/post/create/', view_func=blog.post_create, methods=('GET', 'POST'))
blog.blog_bp.add_url_rule('/post/view/', view_func=blog.post_details, methods=('GET',))
blog.blog_bp.add_url_rule('/post/update/', view_func=blog.post_update, methods=('GET', 'POST'))
blog.blog_bp.add_url_rule('/post/delete/', view_func=blog.post_delete, methods=('GET',))
blog.blog_bp.add_url_rule('/category/', view_func=blog.post_by_categories, methods=('GET',))
blog.blog_bp.add_url_rule('/me/', view_func=blog.profile, methods=('GET',))
blog.blog_bp.add_url_rule('/add-comment/', view_func=blog.add_comment, methods=('POST',))
