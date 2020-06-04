#/bin/env python3

import sys
import os
import json

"""
Quick-n-dirty

TO-DO
[ ] Convert to class
[ ] Handle post body itself
"""


def write_md(posts, p_tag_map):
    print(len(posts))

    for post in posts:
#        print(post["id"])
#        print(post["title"].encode("utf-8"))
#        print(post["slug"])
#        print(post["feature_image"])
#        print(post["status"])
#        print(post["created_at"])
#        print(post["type"])

        # do not process draft
        if post["status"] == "draft":
            continue

        pub_date = post["created_at"].split()
        pub_year = pub_date[0].split("-")[0]
        pub_month = pub_date[0].split("-")[1]

        with open("%s.md" %(post["slug"]), "w") as md:
            md.write("---\n")
            md.write("""title: "%s"  \n""" %(post["title"].encode("utf-8")))
            md.write("""date: "%sT%s+09:00"  \n""" %(pub_date[0], pub_date[1]))
            md.write("""year: "%s"  \n""" %(pub_year))
            md.write("""month: "%s/%s"  \n""" %(pub_year, pub_month))
            md.write("""categories: ["%s"]  \n""" %"note")
            if post["id"] in p_tag_map:
                md.write("""tags: %s  \n""" %p_tag_map[post["id"].encode("utf-8")])
            md.write("---\n\n")
            md.write(post["plaintext"].encode("utf-8"))

def build_tag_map(tags):
    tag_list = {}
    for tag in tags:
        tag_list[tag["id"].encode("utf-8")] = tag["slug"].encode("utf-8")

#    for tag_id in tag_map:
#        print(tag_id, tag_map[tag_id])

    return tag_list

def build_post2tag_map(posts_tags, tag_map):
    """build posts_tag list with the post_id as key
    """
    p_tag_map = {}
    for p_tag in posts_tags:
        post_id = p_tag["post_id"]
        tag_id = p_tag["tag_id"]

        if post_id in p_tag_map:
            p_tag_map[post_id].append(tag_map[tag_id].encode("utf-8"))
        else:
            p_tag_map[post_id] = [tag_map[tag_id].encode("utf-8")]

#    for p_tag in p_tag_map:
#        print(p_tag, p_tag_map[p_tag])

    return p_tag_map

with open(sys.argv[1], 'r') as f:
    data = json.load(f)

    posts = data['db'][0]['data']['posts']
    posts_tags = data['db'][0]['data']['posts_tags']
    tags = data['db'][0]['data']['tags']

    tag_map = build_tag_map(tags)
    p_tag_map = build_post2tag_map(posts_tags, tag_map)

    write_md(posts, p_tag_map)
