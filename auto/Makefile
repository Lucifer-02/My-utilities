DIR = ${DATA_PATH}

pull-stats:
	cd $(DIR)/stats-practices/ && git pull && cd

pull_gopl:
	cd $(DIR)/gopl/ && git pull && cd

pull-music:
	cd $(DIR)/music-theory/ && git pull && cd

pull-tool:
	cd $(DIR)/My-utilities/ && git pull && cd

stat:
	xdotool selectwindow | xsel -ib
	nvim ./My-utilities/config.json
	python3 $(DIR)/My-utilities/auto/auto_stats.py

go:
	ebook-viewer --detach $(DIR)/gopl/the_go_programming_language.epub 
	sleep 1
	xdotool key 'Super_L+Left'
	sleep 0.5
	xdotool key 'Alt+Tab'
	sleep 0.5
	xdotool key 'Super_L+Right'
	sleep 0.5
	xdotool type 'cd gopl/ch1' ; xdotool key Return
	sleep 0.5
	xfce4-terminal --tab -T 'auto' --command 'nvim /home/lucifer/.config/nvim/lua/custom/mappings.lua'

music:
	ebook-edit music-theory/music_theory_for_guitarists_the_complete_method_book_James.epub

test:
	xdotool type 'cd gopl/ch1' ; xdotool key Return
	

pull: pull-stats pull-music pull-tool pull_gopl
