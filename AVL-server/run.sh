#!/bin/bash
source config

avl_stop(){
	[[ ! -f $processid ]] && return
	kill $(cat $processid) > /dev/null 2>&1
	rm $processid
}

start_api() {
    avl_stop
	python app.py > /dev/null 2>&1 & echo "$!" >> $processid
}

start_localhost() {
	start_api
	API_URL="http://$HOST:$API_PORT" 
	show_result
}

start_cloudflared() { 
	isOnline=$(ping -q -c1 google.com &>/dev/null) 
	if [ ! isOnline ]; then
		echo "You are offline, check your connection...." 
		sleep 2
		tunnel_menu
		return
	fi

	start_api 

	rm -f $server_log
	.server/cloudflared tunnel -url "$HOST":"$API_PORT" --logfile  $server_log > /dev/null 2>&1 & echo "$!" >> $processid

	while [ ! $API_URL ]
	do
		API_URL=$(grep -so 'https://[-0-9a-z]*\.trycloudflare.com' "$server_log")
		sleep 0.2
	done
	show_result
}

show_result() {
	[[ -z "$API_URL" ]] && return;

	clear

	echo -e "\nAPI: $API_URL"
	echo $API_URL > $tmp_api
}

tunnel_menu() {
	clear 

	cat <<- EOF
		[01] Local   
		[02] Online
		[03] Copy
		[04] Stop
		[05] Reset
	EOF

	read -p "Your option:"

	case $REPLY in 
		1 | 01)
			start_localhost ;;
		2 | 02)
			start_cloudflared ;;
		3 | 03)
			xclip -i $tmp_api -sel c ;;
		4 | 04)
			avl_stop ;;
		5 | 05)
			avl_stop 
			rm -rf $CACHE_DIR ;;
		*)
			echo -ne "\nInvalid Option, Try Again...\n"
			sleep 0.5
			tunnel_menu
			;;
	esac
}

tunnel_menu
