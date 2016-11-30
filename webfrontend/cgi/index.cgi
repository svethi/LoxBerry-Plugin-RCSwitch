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

use CGI::Carp qw(fatalsToBrowser);
use CGI qw/:standard/;
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


# Calculate Elro commands
if ( param('type')  eq "elro" ) {

  our $valueb0 = param('b[0]');
  if ( $valueb0 ) { our $statusb0 = "on" } else { our $statusb0 = "off" };
  our $valueb1 = param('b[1]');
  if ( $valueb1 ) { our $statusb1 = "on" } else { our $statusb1 = "off" };
  our $valueb2 = param('b[2]');
  if ( $valueb2 ) { our $statusb2 = "on" } else { our $statusb2 = "off" };
  our $valueb3 = param('b[3]');
  if ( $valueb3 ) { our $statusb3 = "on" } else { our $statusb3 = "off" };
  our $valueb4 = param('b[4]');
  if ( $valueb4 ) { our $statusb4 = "on" } else { our $statusb4 = "off" };
  our $valueb5 = param('b[5]');
  if ( $valueb5 ) { our $statusb5 = "on" } else { our $statusb5 = "off" };
  our $valueb6 = param('b[6]');
  if ( $valueb6 ) { our $statusb6 = "on" } else { our $statusb6 = "off" };
  our $valueb7 = param('b[7]');
  if ( $valueb7 ) { our $statusb7 = "on" } else { our $statusb7 = "off" };
  our $valueb8 = param('b[8]');
  if ( $valueb8 ) { our $statusb8 = "on" } else { our $statusb8 = "off" };
  our $valueb9 = param('b[9]');
  if ( $valueb9 ) { our $statusb9 = "on" } else { our $statusb9 = "off" };

  if ( ($valueb0 + $valueb1 + $valueb2 + $valueb3 + $valueb4) eq 1 ) {
	if ( param('b[0]') ) { our $group1 = "1" }
	elsif ( param('b[1]') ) { our $group1 = "2" }
	elsif ( param('b[2]') ) { our $group1 = "3" }
	elsif ( param('b[3]') ) { our $group1 = "4" }
	elsif ( param('b[4]') ) { our $group1 = "5" }
	else { our $group1 = "0" } ;
  } else {
	our $group1 = "$valueb0$valueb1$valueb2$valueb3$valueb4";
	if ( $group1 eq "" ) { $group1 = "0"; }
  }

  if ( ($valueb5 + $valueb6 + $valueb7 + $valueb8 + $valueb9) eq 1 ) {
	if ( param('b[5]') ) { our $unit1 = "1" }
	elsif ( param('b[6]') ) { our $unit1 = "2" }
	elsif ( param('b[7]') ) { our $unit1 = "3" }
	elsif ( param('b[8]') ) { our $unit1 = "4" }
	elsif ( param('b[9]') ) { our $unit1 = "5" }
	else { our $unit1 = "0" } ;
  } else {
	our $unit1 = "$valueb0$valueb1$valueb2$valueb3$valueb4";
	if ( $unit1 eq "" ) { $unit1 = "0"; }
  }

} else {

  our $statusb0 = "off";
  our $valueb0 = "0";
  our $statusb1 = "off";
  our $valueb1 = "0";
  our $statusb2 = "off";
  our $valueb2 = "0";
  our $statusb3 = "off";
  our $valueb3 = "0";
  our $statusb4 = "off";
  our $valueb4 = "0";
  our $statusb5 = "off";
  our $valueb5 = "0";
  our $statusb6 = "off";
  our $valueb6 = "0";
  our $statusb7 = "off";
  our $valueb7 = "0";
  our $statusb8 = "off";
  our $valueb8 = "0";
  our $statusb9 = "off";
  our $valueb9 = "0";
  our $group1 = "0";
  our $unit1 = "0";

}

# Calculate Intertechno commands
if ( param('type')  eq "intertechno" ) {

  our $family2 = param('family');
  if ( $family2 eq "A" ) { our $selectedA = "selected=selected" }
  elsif ( $family2 eq "B" ) { our $selectedB = "selected=selected" }
  elsif ( $family2 eq "C" ) { our $selectedC = "selected=selected" }
  elsif ( $family2 eq "D" ) { our $selectedD = "selected=selected" }
  elsif ( $family2 eq "E" ) { our $selectedE = "selected=selected" }
  elsif ( $family2 eq "F" ) { our $selectedF = "selected=selected" }
  elsif ( $family2 eq "G" ) { our $selectedG = "selected=selected" }
  elsif ( $family2 eq "H" ) { our $selectedH = "selected=selected" }
  elsif ( $family2 eq "I" ) { our $selectedI = "selected=selected" }
  elsif ( $family2 eq "J" ) { our $selectedJ = "selected=selected" }
  elsif ( $family2 eq "K" ) { our $selectedK = "selected=selected" }
  elsif ( $family2 eq "L" ) { our $selectedL = "selected=selected" }
  elsif ( $family2 eq "M" ) { our $selectedM = "selected=selected" }
  elsif ( $family2 eq "N" ) { our $selectedN = "selected=selected" }
  elsif ( $family2 eq "O" ) { our $selectedO = "selected=selected" }
  elsif ( $family2 eq "P" ) { our $selectedP = "selected=selected" };

  our $unittemp = param('unit');
  if ( $unittemp eq "1" ) { our $selected1 = "selected=selected" }
  elsif ( $unittemp eq "2" ) { our $selected2 = "selected=selected" }
  elsif ( $unittemp eq "3" ) { our $selected3 = "selected=selected" }
  elsif ( $unittemp eq "4" ) { our $selected4 = "selected=selected" }
  elsif ( $unittemp eq "5" ) { our $selected5 = "selected=selected" }
  elsif ( $unittemp eq "6" ) { our $selected6 = "selected=selected" }
  elsif ( $unittemp eq "7" ) { our $selected7 = "selected=selected" }
  elsif ( $unittemp eq "8" ) { our $selected8 = "selected=selected" }
  elsif ( $unittemp eq "9" ) { our $selected9 = "selected=selected" }
  elsif ( $unittemp eq "10" ) { our $selected10 = "selected=selected" }
  elsif ( $unittemp eq "11" ) { our $selected11 = "selected=selected" }
  elsif ( $unittemp eq "12" ) { our $selected12 = "selected=selected" }
  elsif ( $unittemp eq "13" ) { our $selected13 = "selected=selected" }
  elsif ( $unittemp eq "14" ) { our $selected14 = "selected=selected" }
  elsif ( $unittemp eq "15" ) { our $selected15 = "selected=selected" }
  elsif ( $unittemp eq "16" ) { our $selected16 = "selected=selected" };

  if ( $unittemp > 0 && $unittemp <= 4) {
    our $group2 = "1";
    our $unit2 = $unittemp;
  }
  elsif ( $unittemp > 4 && $unittemp <= 8) {
    our $group2 = "2";
    our $unit2 = $unittemp - 4;
  }
  elsif ( $unittemp > 8 && $unittemp <= 12) {
    our $group2 = "3";
    our $unit2 = $unittemp - 8;
  }
  elsif ( $unittemp > 12 && $unittemp <= 16) {
    our $group2 = "4";
    our $unit2 = $unittemp - 12;
  }

} else {

  our $family2 = "0";
  our $group2 = "0";
  our $unit2 = "0";

}

# Some vars for the template
our $host = "$ENV{HTTP_HOST}";
our $loginname = "$ENV{REMOTE_USER}";

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
