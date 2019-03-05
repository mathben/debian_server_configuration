#!/usr/bin/env python3
import json
import os
import sys

ROOT_DIR = os.path.normpath(os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", ".."))
NGINX_CONF = os.path.join(ROOT_DIR, "conf", "nginx.json")
NGINX_TEMPLATE_SITE = os.path.join(ROOT_DIR, "template", "nginx_server_site_template")
IGNORED_DIR = (".idea",)


def main():
    # Validate conf file exist
    if not os.path.exists(NGINX_CONF):
        msg_err = "File %s not exist." % NGINX_CONF
        print(msg_err, file=sys.stderr)
        sys.exit(1)

    # NGINX configuration
    with open(NGINX_CONF, encoding='utf-8') as nginx_conf_file:
        nginx_conf = json.load(nginx_conf_file)

    use_demo_data = nginx_conf.get("use_demo_data", False)
    http_dir = nginx_conf.get("server_http_project_dir")
    etc_nginx_dir = nginx_conf.get("etc_nginx")

    etc_nginx_sites_available_dir = os.path.join(etc_nginx_dir, "sites-available")
    etc_nginx_sites_enabled_dir = os.path.join(etc_nginx_dir, "sites-enabled")
    if not os.path.exists(etc_nginx_dir):
        os.mkdir(etc_nginx_dir)
        os.mkdir(etc_nginx_sites_available_dir)
        os.mkdir(etc_nginx_sites_enabled_dir)

    # NGINX template site
    with open(NGINX_TEMPLATE_SITE, encoding='utf-8') as nginx_template_file:
        template_nginx_site = nginx_template_file.read()

    lst_dir_site = os.listdir(http_dir)
    for dir_site in lst_dir_site:
        if dir_site in IGNORED_DIR:
            continue

        site_content = template_nginx_site.replace("$SERVER_NAME", dir_site)
        site_content = site_content.replace("$SERVER_ROOT", os.path.join(http_dir, dir_site))
        new_sites_available = os.path.join(etc_nginx_sites_available_dir, dir_site)
        new_sites_enabled = os.path.join(etc_nginx_sites_enabled_dir, dir_site)

        os.remove(new_sites_available)
        with open(new_sites_available, "w", encoding='utf-8') as new_nginx_file:
            new_nginx_file.write(site_content)

        os.remove(new_sites_enabled)
        os.symlink(new_sites_available, new_sites_enabled)


if __name__ == '__main__':
    main()
