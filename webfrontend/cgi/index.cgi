#!/usr/bin/perl

# Copyright 2016 Michael Schlenstedt, michael@loxberry.de
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


##########################################################################
# Modules
##########################################################################

use Config::Simple;
use File::HomeDir;
use Cwd 'abs_path';
#use warnings;
#use strict;
#no strict "refs"; # we need it for template system

##########################################################################
# Variables
##########################################################################

our $cfg;
our $lang;
our $template_title;
our $help;
our @help;
our $helptext;
our $helplink;
our $installfolder;
our $version;
my  $home = File::HomeDir->my_home;
our $psubfolder;

##########################################################################
# Read Settings
##########################################################################

# Version of this script
$version = "0.0.1";

# Figure out in which subfolder we are installed
$psubfolder = abs_path($0);
$psubfolder =~ s/(.*)\/(.*)\/(.*)$/$2/g;

$cfg             = new Config::Simple("$home/config/system/general.cfg");
$installfolder   = $cfg->param("BASE.INSTALLFOLDER");
$lang            = $cfg->param("BASE.LANG");

# Init Language
# Clean up lang variable
$lang =~ tr/a-z//cd;
$lang = substr($lang,0,2);

# If there's no file in our language, use german as default
if (!-e "$installfolder/templates/plugins/$psubfolder/$lang/main.html") {
	$lang = "de";
}

##########################################################################
# Main program
##########################################################################

print "Content-Type: text/html\n\n";

# Vars for template
$template_title = "LoxBerry: RCSwitch Plugin";

# Print Template

# Create Help page
$helplink = "http://www.loxwiki.eu:80/x/JATL";
open(F,"$installfolder/templates/plugins/$psubfolder/$lang/help.html") || die "Missing template plugins/$psubfolder/$lang/help.html";
  @help = <F>;
  foreach (@help)
  {
    s/[\n\r]/ /g;
    $_ =~ s/<!--\$(.*?)-->/${$1}/g;
    $helptext = $helptext . $_;
  }
close(F);

# Header
open(F,"$installfolder/templates/system/$lang/header.html") || die "Missing template system/$lang/header.html";
  while (<F>) 
  {
    $_ =~ s/<!--\$(.*?)-->/${$1}/g;
    print $_;
  }
close(F);

# Main
open(F,"$installfolder/templates/plugins/$psubfolder/$lang/main.html") || die "Missing template plugins/$psubfolder/$lang/main.html";
while (<F>) 
  {
    $_ =~ s/<!--\$(.*?)-->/${$1}/g;
    print $_;
  }
close(F);

# Footer
open(F,"$installfolder/templates/system/$lang/footer.html") || die "Missing template system/$lang/footer.html";
  while (<F>) 
  {
    $_ =~ s/<!--\$(.*?)-->/${$1}/g;
    print $_;
  }
close(F);

exit;
