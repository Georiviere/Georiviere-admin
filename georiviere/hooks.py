def preprocessing_filter_spec(endpoints):
    filtered = []
    for (path, path_regex, method, callback) in endpoints:
        # Remove all but DRF API endpoints
        if path.startswith("/api/portal/"):
            filtered.append((path, path_regex, method, callback))
    return filtered
