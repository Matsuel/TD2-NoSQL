def format_user(user):
    """
    Format a user node into a dictionary.
    """
    return {
        "id": user.identity,
        "name": user["name"],
        "email": user["email"],
        "created_at": user["created_at"]
    }
    
def format_post(post):
    """
    Format a post node into a dictionary.
    """
    return {
        "id": post.identity,
        "title": post["title"],
        "content": post["content"],
        "created_at": post["created_at"]
    }
    
def format_comment(comment):
    """
    Format a comment node into a dictionary.
    """
    return {
        "id": comment.identity,
        "content": comment["content"],
        "created_at": comment["created_at"]
    }