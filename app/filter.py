def filter_apps(apps, keywords=None, exclude_keywords=None):
    keywords = keywords or []
    exclude_keywords = exclude_keywords or []
    filtered = []
    for app in apps:
        title = app["title"].lower()
        desc = app["desc"].lower()
        if any(bad in title or bad in desc for bad in exclude_keywords):
            continue
        if not keywords or any(kw in title or kw in desc for kw in keywords):
            filtered.append(app)
    return filtered
