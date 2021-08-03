from flaskr.blog import blog

blog.blog_bp.add_url_rule('/', view_func=blog.home, methods=('GET',))
blog.blog_bp.add_url_rule('/contact/', view_func=blog.contact, methods=('GET', 'POST',))
blog.blog_bp.add_url_rule('/author/', view_func=blog.author_details, methods=('GET',))
blog.blog_bp.add_url_rule('/post/create/', view_func=blog.post_create, methods=('GET', 'POST'))
blog.blog_bp.add_url_rule('/post/view/', view_func=blog.post_details, methods=('GET',))
blog.blog_bp.add_url_rule('/post/update/', view_func=blog.post_create, methods=('GET',))
blog.blog_bp.add_url_rule('/post/delete/', view_func=blog.post_create, methods=('POST',))
blog.blog_bp.add_url_rule('/category/', view_func=blog.post_by_categories, methods=('GET',))
blog.blog_bp.add_url_rule('/me/', view_func=blog.me_details, methods=('GET',))
blog.blog_bp.add_url_rule('/me/posts/', view_func=blog.post_by_categories, methods=('GET',))
blog.blog_bp.add_url_rule('/me/settings/', view_func=blog.post_by_categories, methods=('GET',))