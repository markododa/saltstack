#!/bin/bash 
mkdir /etc/e2guardian/lists/blacklists/ -p

KRUG=0
while [  $KRUG -lt 3 ]; do
case $KRUG in
0)
  PRE='mkdir -p /etc/e2guardian/lists/blacklists/'
  POS=''
  ;;
1)
  PRE='touch /etc/e2guardian/lists/blacklists/'
  POS='/urls'
  ;;
2)
  PRE='touch /etc/e2guardian/lists/blacklists/'
  POS='/domains'
  ;;
esac

eval "$PRE"_custom"$POS"
eval "$PRE"adult"$POS"
eval "$PRE"aggressive"$POS"
eval "$PRE"alcohol"$POS"
eval "$PRE"astrology"$POS"
eval "$PRE"banking"$POS"
eval "$PRE"bitcoin"$POS"
eval "$PRE"books"$POS"
eval "$PRE"chat"$POS"
eval "$PRE"cleaning"$POS"
eval "$PRE"clothing"$POS"
eval "$PRE"cooking"$POS"
eval "$PRE"dating"$POS"
eval "$PRE"drugs"$POS"
eval "$PRE"ecommerce"$POS"
eval "$PRE"entertainment"$POS"
eval "$PRE"filesharing"$POS"
eval "$PRE"financial"$POS"
eval "$PRE"forums"$POS"
eval "$PRE"gambling"$POS"
eval "$PRE"games"$POS"
eval "$PRE"gardening"$POS"
eval "$PRE"government"$POS"
eval "$PRE"guns"$POS"
eval "$PRE"hacking"$POS"
eval "$PRE"humor"$POS"
eval "$PRE"hygiene"$POS"
eval "$PRE"jobsearch"$POS"
eval "$PRE"lingerie"$POS"
eval "$PRE"magazines"$POS"
eval "$PRE"mail"$POS"
eval "$PRE"malware"$POS"
eval "$PRE"medical"$POS"
eval "$PRE"news"$POS"
eval "$PRE"pets"$POS"
eval "$PRE"phishing"$POS"
eval "$PRE"porn"$POS"
eval "$PRE"press"$POS"
eval "$PRE"proxy"$POS"
eval "$PRE"radio"$POS"
eval "$PRE"redirector"$POS"
eval "$PRE"religion"$POS"
eval "$PRE"sect"$POS"
eval "$PRE"sexuality"$POS"
eval "$PRE"shopping"$POS"
eval "$PRE"shortener"$POS"
eval "$PRE"sports"$POS"
eval "$PRE"spyware"$POS"
eval "$PRE"tobacco"$POS"
eval "$PRE"warez"$POS"
eval "$PRE"weapons"$POS"
eval "$PRE"weather"$POS"
eval "$PRE"webmail"$POS"

let KRUG=KRUG+1
done



