def parse_arguments(arguments):
    topics = {}
    for argument, topic_name in zip(arguments, arguments[1:]):
        if argument == "--topic":
            topics[topic_name] = {"name": topic_name}
    return {"topics": topics}

