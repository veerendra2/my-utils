#!/usr/bin/env bash
# Automated script to install Ruby2.4, Jekyll and its gems in Ubuntu 14.04

sudo apt-add-repository ppa:brightbox/ruby-ng -y
sudo apt-get update
sudo apt-get install make g++ ruby2.4 ruby2.4-dev zlib1g-dev -y
sudo gem install jekyll bundler
echo "** Installing Jekyll related GEMs **"
sudo gem install rdoc
sudo gem install jekyll-sitemap
sudo gem install jekyll-feed
sudo gem install jekyll-assets
sudo gem install jekyll-redirect-from
sudo gem install jekyll-paginate
