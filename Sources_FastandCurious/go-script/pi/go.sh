#!/bin/bash
#Donkey Car Start menu
#-------------------------------------------
# v0.1 - 03/2021
# by Fast & Curious
#-------------------------------------------

#-------------------------------------------
# Variables
#-------------------------------------------

	carsPath="/home/pi/fc_cars" 					# Emplacement de dossiers MyCar
	modelsPath="/models" 							# Nom du sous-dossier contenant les modèles
	dataPath="/data" 								# Nom du sous-dossier contenant les données (Tubs)
	car=""
	model=""
	jsPath="/dev/input/js0" 						# Emplacement du joystick
	baseDonkeyPath="/home/pi/projects/donkeycar-fc" # Emplacement du dossier de base DonkeyCar
  pidfile="/tmp/go.pid"

#-------------------------------------------
# Fonctions
#-------------------------------------------

	#Logo
	function logo()
	{
		clear
		echo
		echo -e '\e[38;5;118m ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄'
		echo -e '\e[38;5;119m __________              __       ___      _________                _                     '
		echo -e '\e[38;5;120m ___  ____/___ _________  /_   __( _ )     __  ____/___  __________(_)_________  _________'
		echo -e '\e[38;5;121m __  /_ _  __ `/_  ___/  __/   _  __ \/|   _  /    _  / / /_  __/_  /_  __ \  / / /_  ___/'
		echo -e '\e[38;5;122m _  __/ / /_/ /_(__  )/ /_     / /_/  <    / /___  / /_/ /_  /  _  / / /_/ / /_/ /_(__  ) '
		echo -e '\e[38;5;123m /_/    \__,_/ /____/ \__/     \____/\/    \____/  \__,_/ /_/   /_/  \____/\__,_/ /____/  '
		echo
		echo -e '\e[38;5;159m ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄ D O N K E Y    C A R    G O ! ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄'
		echo
		echo
		echo -e "\e[39m"
	}

	function mainmenu()
	{
		logo
		echo -e "\e[92m ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄"
		echo
		echo -e "\e[97m Choose an option :"
		echo
		echo -e "\e[97m  1) Start donkey car in DRIVING mode with JOYSTICK"
		echo -e "\e[97m  2) Start donkey car in DRIVING mode with WEB CONTROLLER"
		echo -e "\e[97m  3) Compress and empty car data folder"
		echo
		echo -e "\e[36m  4) Start donkey car in AUTOPILOT mode"
		echo
		echo -e "\e[97m  5) Update car from donkey car package"
		echo
		echo -e "\e[97m  8) Git operations"
		echo -e "\e[97m  9) Display software versions"
		echo
		echo -e "\e[97m  0) Quit "
		echo -e "\e[92m ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄"
		echo -e "\e[39m"
		
		read a
		case $a in
			1) start-driving ; mainmenu ;;
			2) start-drivingweb ; mainmenu ;;
			3) compress-data ; mainmenu ;;
			4) start-autopilot ; mainmenu ;;
			5) update-car ; mainmenu ;;
			8) git-tools ; mainmenu ;;
			9) stats ; mainmenu ;;
			0) clear ; echo -e "\e[39m Bye !" ; return 0 ;;
			*) echo -e "Wrong option" ; mainmenu ;;
		esac
	}

	function carmenu()
	{
		logo 
		
		#Looking for all cars in carsPath
		unset options directories
		for directory in $carsPath/*/; do
			option=$(basename "$directory")
			options[directories++]=$option
		done
		
		echo -e "\e[92m ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄"
		echo -e "\e[97m  Choose an car in $carsPath :"
		echo
		
		select opt in "${options[@]}"; do
		  echo "  Selected car $opt"
		  echo
		  car="$carsPath/$opt"
		  break
		done
	}


	function modelmenu()
	{		
		#Looking for all model in car
		unset options directories
		for file in $car$modelsPath/*.{h5,tflite,xml} ; do
			option=$(basename "$file")
			options[directories++]=$option
		done
		
		echo -e "\e[92m ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄"
		echo -e "\e[97m  Choose an model in $car$modelPath :"
		echo  "  .h5 : Keras model  |  .tflite : TensorFlow lite model  |  .xml : Openvino model"
		echo
		
		select opt in "${options[@]}"; do
		  echo "  Selected model $opt"
		  echo
		  model="$car$modelsPath/$opt"
		  break
		done
	}
	
	
	function pause()
	{
		echo
		echo -e "\e[92m ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄"
		echo -e "\e[92m  Press a key to return to continue..."
		read a
	}


	function start-driving()
	{
		carmenu
		logo
		
		if [[ $(ls $jsPath) ]]
		then
			echo -e "\e[97m  $jsPath found !"
			cd $car
			commandline="python manage.py drive --js"
			
			echo -e "\e[92m  Starting Donkey Car in learning mode..."
			echo -e "\e[92m ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄"
			echo
			echo -e "\e[97m  Current folder : $car"
			echo -e "\e[97m  Command line   : $commandline"
			echo -e "\e[39m"
			
			$commandline
		else
			echo -e "\e[91m" "  Joystick not found at $jsPath !"
		fi
		
		pause
	}


	function start-drivingweb()
	{
		carmenu
		logo
		
		cd $car
		commandline="python manage.py drive"
		
		echo -e "\e[92m  Starting Donkey Car in learning mode..."
		echo -e "\e[92m ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄"
		echo
		echo -e "\e[97m  Current folder : $car"
		echo -e "\e[97m  Command line   : $commandline"
		echo -e "\e[39m"
		
		$commandline
		
		pause
	}


	function start-autopilot()
	{
		carmenu
		modelmenu
		logo
		
		cd $car

		modeltype=""
		if [[ $model == *'.tflite'* ]]
		then
			modeltype="--type=tflite_linear"	
		fi
		commandline="python manage.py drive --model $model $modeltype"
		
		echo -e "\e[92m  Starting Donkey Car in autopilot mode... May the force be with you !"
		echo -e "\e[92m ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄"
		echo
		echo -e "\e[97m  Current folder : $car"
		echo -e "\e[97m  Command line   : $commandline"
		echo -e "\e[39m"
		
		$commandline
		
		pause
	}


	function stats()
	{
		logo
		
		echo -e "\e[92m  Current software versions :"
		echo -e "\e[92m ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄"
		echo -e "\e[97m"
		
		echo "OS VERSION :"
		osversion=$(cat /etc/os-release | grep PRETTY)
		echo ${osversion/PRETTY_NAME=/""}
		cat /etc/rpi-issue | grep reference
		uname -sr
		
		echo
		echo "PYTHON VERSION :"
		python --version
		
		echo
		echo "MAIN PIP MODULES :"
		pip list | grep 'donkeycar\|tensorflow\|opencv\|openvino'
		
		pause
	}


	function compress-data()
	{
		carmenu
		logo
		
			
		echo
		echo " Compressing $car/data folder..."
		commandline="zip -r -1 $car/$(date +"%Y%m%d-%H%M%S")-data.zip $car/data/*"
		$commandline
		echo
		echo " File $car/$(date +"%Y%m%d-%H%M%S") created in car folder."

		echo
		echo " Deleting data folder content..."
		commandline="rm -rf $car/data/*"
		$commandline
		echo
		echo " Done."
		
		pause
	}


	function update-car()
	{
		carmenu
		logo
		
		cd $car
		commandline="donkey update"
		
		echo -e "\e[92m  Update car from donkey car package"
		echo -e "\e[92m ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄"
		echo
		echo -e "\e[97m  Current folder : $car"
		echo -e "\e[97m  Command line   : $commandline"
		echo -e "\e[39m"
		
		$commandline
		
		pause
	}

	function git-tools()
	{
		logo

		cd $baseDonkeyPath
		branch=$(git branch)
		remoteRepo=$(git config --get remote.origin.url)

		echo -e "\e[92m ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄"
		echo
		echo -e "\e[97m Local folder : $baseDonkeyPath"
		echo -e "\e[97m Remote repository : $remoteRepo"
		echo -e "\e[97m Current branch : $branch"
		echo
		echo -e "\e[97m Choose a GIT operation :"
		echo
		echo -e "\e[97m  1) PULL remote updates from repository"
		echo -e "\e[97m  2) PUSH local updates to repository"
		echo
		echo -e "\e[97m  0) Back"
		echo -e "\e[92m ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄"
		echo -e "\e[39m"
		
		read a
		case $a in
			1) git-pull ;;
			2) git-push ;;
			0) ;;
		esac
	}

	function git-pull()
	{
		logo

		cd $baseDonkeyPath
		branch=$(git branch)
		remoteRepo=$(git config --get remote.origin.url)
		
		echo -e "\e[92m  Pushing local updates to repository :"
		echo -e "\e[92m ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄"
		echo -e "\e[97m"
		echo -e "\e[97m Local folder : $baseDonkeyPath"
		echo -e "\e[97m Remote repository : $remoteRepo"
		echo -e "\e[97m Current branch : $branch"
		echo -e "\e[39m"
		
		git pull

		pause
	}

	function git-push()
	{
		logo

		cd $baseDonkeyPath
		branch=$(git branch)
		remoteRepo=$(git config --get remote.origin.url)
		
		echo -e "\e[92m  Pushing local updates to repository :"
		echo -e "\e[92m ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄"
		echo -e "\e[97m"
		echo -e "\e[97m Local folder : $baseDonkeyPath"
		echo -e "\e[97m Remote repository : $remoteRepo"
		echo -e "\e[97m Current branch : $branch"
		echo -e "\e[39m"
		
		
		read  -p "Commit message :" commitmessage
		git add *
		git commit -m "$commitmessage"
		git push

		pause
	}

#-------------------------------------------
# Main
#-------------------------------------------
pid=$$

if [ -f $pidfile ]; then
  kill -0 $(cat $pidfile)
  if [ $? == 0 ]; then
    echo "Already launched, exiting"
    exit 1
  else
    echo "Remove old pidfile"
    rm -f $pidfile
  fi
fi
echo $pid > $pidfile

mainmenu
retour=$?
rm -f $pidfile
exit $retour