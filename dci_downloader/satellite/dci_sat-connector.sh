#! /usr/bin/bash

set -v


# dci_sat-connector [topic] [dest_repo] [-nd] [-lcm]
# topic and dest_repo same as dci-downloader args
# -nd and -lcm are options
# -nd is set to disable topic download when locally present
# -lcm is set to create repo Content VIew and associated lifecycle management states
# Example:  dci_sat-connector.sh RHEL-8-milestone http://pctt-hv4/pub/dci/ -lcm
#           assumes directory /dci created manually within standard Satellite server public repo dir.

topic=$1
dest_repo=$2
no_dwnld=0
lcm=0
var=0
the_org="Red Hat"
prod_name="DCI "$topic" Product"
repo_name="DCI "$topic" Repository"
cv_name="DCI "$topic" Content View"
lcm_qa_name="DCI "$topic" LCM QA"
lcm_dev_name="DCI "$topic" LCM Dev"
lcm_prod_name="DCI "$topic" LCM Prod"

# Command Line Parsing/Checking
if [ -z "$1" -o $# -lt 2 -o $# -gt 4 ]; then
  echo "ERROR dci_sat-connector [topic] [dest_repo] [-nd] [-lcm]"
  exit 1

elif [ $# == 3 ]; then
  if [ $3 == "-nd" ]; then
    no_dwnld=1
  elif [ $3 == "-lcm" ]; then
    lcm=1
  else
    echo "ERROR dci_sat-connector [topic] [dest_repo] [-nd] [-lcm]"
    exit 1
  fi
elif [ $4 == "-nd" ]; then
    no_dwnld=1
  elif [ $4 == "-lcm" ]; then
    lcm=1
  else
    echo "dci_sat-connector [topic] [dest_repo] [-nd] [-lcm]"
    exit 1
fi

echo "no_dwnld = $no_dwnld,  lcm = $lcm"
for var; do
  echo $var
done

# Get Topic Repo
if [ $no_downld ]; then
  dci-downloader $topic $dest_repo
fi

# Import Custom Product into Satellite
hammer product create --name="$prod_name"  --organization="$the_org" --description="Automated description for"

hammer repository create --name="$repo_name"  --organization="$the_org" --product="$prod_name"  --content-type=yum --download-policy=immediate --url=""$dest_repo"/"$topic"/compose/BaseOS/x86_64/os/"

hammer repository synchronize --name="$repo_name" --product="$prod_name" --organization="$the_org"

if [ create_lcm ]; then
  # Create the lifecycle
  hammer lifecycle-environment create --organization="$the_org" --name="$lcm_dev_name" --description="Automated description for" --prior="Library"
  hammer lifecycle-environment create --organization="$the_org" --name="$lcm_qa_name"  --description="Automated description for" --prior="$le_dev_name"
  hammer lifecycle-environment create --organization="$the_org" --name="$lcm_prod_name" --description="Automated description for" --prior="$le_qa_name"

  # Create one or more content views i.e. rinse repeat
  # a content view is used to restrict the view of an individual host to a given set of content in a given life cycle environment.
  hammer content-view create --organization="$the_org" --name="$cv_name"  --description=" Content View"
  hammer content-view add-repository --organization="$the_org" --name="$cv_name" --product="$prod_name" --repository="$repo_name"

  # repeat to add more repositories to the view.
  # more repos means an individual host sees more stuff.

  #Publish the content view to the library
  hammer content-view publish --organization="$the_org" --name="$cv_name" --description="Content View Publication"
else
  exit 0
fi
