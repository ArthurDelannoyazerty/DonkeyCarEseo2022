#!/bin/bash
#Donkey Car Start menu (PC Side)
#-------------------------------------------
# v0.1 - 03/2021
# by Fast & Curious
#-------------------------------------------

# VARIABLES :
# -----------------------------------------------------------------------------

	$carsPath = "C:\MySigma\dchilloux\IARacing\fc_cars"                                 # Chemin vers les voitures
	$baseDonkeyPath = "C:\MySigma\dchilloux\IARacing\projects\donkeycar-fc" 			# Chemin vers le dossier de base Donkey (customisé F&C)
	$modelsPath = "\models" 															# Nom du sous-dossier contenant les modèles
	$dataPath = "\data" 														     	# Nom du sous-dossier contenant les modèles

# FUNCTIONS :
# -----------------------------------------------------------------------------

Function Logo
{
	Clear-Host
	Write-Host
	Write-host ' ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄' -ForegroundColor "MAGENTA"
	Write-host ' __________              __       ___      _________                _                     ' -ForegroundColor "DARKBLUE"
	Write-host ' ___  ____/___ _________  /_   __( _ )     __  ____/___  __________(_)_________  _________' -ForegroundColor "BLUE"
	Write-host ' __  /_ _  __ `/_  ___/  __/   _  __ \/|   _  /    _  / / /_  __/_  /_  __ \  / / /_  ___/' -ForegroundColor "BLUE"
	Write-host ' _  __/ / /_/ /_(__  )/ /_     / /_/  <    / /___  / /_/ /_  /  _  / / /_/ / /_/ /_(__  ) ' -ForegroundColor "CYAN"
	Write-host ' /_/    \__,_/ /____/ \__/     \____/\/    \____/  \__,_/ /_/   /_/  \____/\__,_/ /____/  ' -ForegroundColor "CYAN"
	Write-host
	Write-host ' ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄ D O N K E Y    C A R    G O !   (PC SIDE) ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄' -ForegroundColor "MAGENTA"
	Write-host
	Write-host
}


Function MainMenu
{
	do
	{
		Logo
		
		Write-host ' ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄' -ForegroundColor "GREEN"
		Write-Host
		Write-Host " Choose an option :"
		Write-Host
		Write-Host "  1) Start donkey car in DRIVING mode with SIMULATOR"
		Write-Host "  2) Start donkey car in AUTOPILOT mode with SIMULATOR"
		Write-Host
		Write-Host "  3) Start donkey car in LOCAL TRAINING mode to create a model from recorded data"
		Write-Host "  4) Make a MOVIE from data and model"
		Write-Host
		Write-Host "  5) Update car from donkey car package"
		Write-Host
		Write-Host "  8) Git operations"
		Write-Host "  9) Display software versions"
		Write-Host
		Write-Host "  0) Quit"
		Write-Host
		Write-host ' ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄' -ForegroundColor "GREEN"



		 $choice = Read-Host
		 switch ($choice)
		 {
			 '1' {
				 Start-Simulator
			 } '2' {
				 Start-Simulator-Auto
			 } '3' {
			     Start-Training
			 } '4' {
			     Make-Movie
			 } '5' {
				 Update-Car
			 } '8' {
				 Git-tools
			 } '9' {
				 Stats
			 } '0' {
				 Clear-Host
				 Write-Host "Bye ! "
				 return
			 }
		 }
	 }
	until ($choice -eq "0")
}

Function Pause
{
	Write-Host
	Write-host ' ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄' -ForegroundColor "GREEN"
	Write-Host "  Press a key to return to continue..." -ForegroundColor "GREEN"
	Read-Host

}

Function Select-car
{
	Logo
	
	Write-host ' ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄' -ForegroundColor "GREEN"
	Write-Host "  Choose a car in $carsPath :"
	Write-Host "  DONKEY_GYM must be enabled in myconfig.py file for driving mode !" -ForegroundColor "RED"
	Write-Host
	
	$result = Get-ChildItem $carsPath | ?{ $_.PSIsContainer }
	for ($i=0; $i -lt $result.Count; $i++) {
		$name = $result[$i].basename
		Write-Host "$i) $name"
	}

	$choice = Read-Host
	$car = $result[$choice].FullName
	Return $car
}
Function Select-model
{
	Logo
	
	Write-host ' ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄' -ForegroundColor "GREEN"
	Write-Host "  Choose a model in $car :"
	Write-Host "  .h5 : Keras model  |  .tflite : TensorFlow lite model  |  .xml : Openvino model"
	Write-Host
	
	$result = Get-ChildItem $car$modelsPath | Where {($_.extension -like ".h5") -or ($_.extension -like ".tflite") -or ($_.extension -like ".xml")} 
	for ($i=0; $i -lt $result.Count; $i++) {
		$name = $fileName = $result[$i].ToString().Split("\")[-1]
		Write-Host "$i) $name"
	}

	$choice = Read-Host
	$model = $result[$choice].FullName
	Return $model
}

Function Select-data ($allowAll)
{
	$result = Get-ChildItem $car$dataPath | ?{ $_.PSIsContainer }

	Write-Host $result[1].BaseName
	if ($result[0].BaseName -like "images") #Seems to be standard data folder, without Tub subfolders
	{
		Write-Host " Traditionnal data folder detected."
		$data = $($dataPath).Substring(1)
	}
	else {
		
		Logo
	
		Write-host ' ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄' -ForegroundColor "GREEN"
		Write-Host "  Multiple data folders detected. Choose a folder in $dataPath :"
		Write-Host
		if ($allowAll) {Write-Host "a) All folders in data" -ForegroundColor "BLUE"}
		for ($i=0; $i -lt $result.Count; $i++) {
			$name = $result[$i].basename
			Write-Host "$i) $name"
		}

		$choice = Read-Host

		if ($choice -like "a")
		{
			$data = ""
			for ($i=0; $i -lt $result.Count; $i++) {
				$data += $($dataPath).Substring(1) + "\" + $($result[$i].basename) + ","
			}
			$data = $data.Substring(0,$data.Length-1)
		}
		else {
			$data = $result[$choice].FullName	
		}
	}
	Return $data
}

Function Start-Training
{
		
	Logo
	
	Write-Host "  Starting Donkey Car in training mode..." -ForegroundColor "GREEN"
	Write-host ' ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄' -ForegroundColor "GREEN"
	Write-Host
	Write-Host
	Write-Host "   Note : "
	Write-Host "       This options generates a model file from car's data, and the optimize it with OpenVINO."
	Write-Host "       Please put Tubs files with images in car folder now."
	Write-Host

	$car = Select-car
	$carBaseName = Split-Path -Path $car -Leaf
	$data = Select-data ($true)

	logo

	$defaultModelName = $carBaseName + "-mod-" + (Get-Date -Format "yyyy-MM-dd") + "-v"
	add-type -AssemblyName System.Windows.Forms
	[System.Windows.Forms.SendKeys]::SendWait($defaultModelName) #Dirty trick to prefill model name...
	$model = Read-Host "Please enter model name (without extension)"
	$kerasmodel = $model + ".h5"
	$tfmodel = $model + ".pb"
	$tflitemodel = $model + ".tflite"


	Logo
	
	$command = "python train.py --tubs=$data --model=$car$modelsPath\$kerasmodel"

	Write-Host "  Starting Donkey Car in training mode..." -ForegroundColor "GREEN"
	Write-host ' ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄' -ForegroundColor "GREEN"
	Write-Host
	Write-Host ' > PART 1 : Train to Keras model (.h5)' -ForegroundColor "BLUE"
	Write-Host '   PART 2 : Convert Keras model (.h5) to Tensorflow model (.pb)' -ForegroundColor "WHITE"
	Write-Host '   PART 3 : Model optimization to use OpenVINO' -ForegroundColor "WHITE"
	Write-Host '   PART 4 : Convert Keras model (.h5) to TFLite model (.tflite)' -ForegroundColor "WHITE"
	Write-Host
	write-host "  Current folder : $car"
	write-host "  Command line : $command"
	Write-Host

	Set-Location $car
	python train.py --tubs=$data --model=$car$modelsPath\$kerasmodel

	Write-Host
	Write-Host '  Training complete ! Review the logs for errors.' -ForegroundColor "GREEN"
	Pause


	Logo
	
	$command = "python $baseDonkeyPath\scripts\freeze_model.py --model=$car$modelsPath\$kerasmodel --output=$car$modelsPath\$tfmodel"

	Write-Host "  Converting Keras model to TensorFlow model..." -ForegroundColor "GREEN"
	Write-host ' ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄' -ForegroundColor "GREEN"
	Write-Host
	Write-Host '   PART 1 : Train to Keras model (.h5)' -ForegroundColor "GRAY"
	Write-Host ' > PART 2 : Convert Keras model (.h5) to Tensorflow model (.pb)' -ForegroundColor "BLUE"
	Write-Host '   PART 3 : Model optimization to use OpenVINO' -ForegroundColor "WHITE"
	Write-Host '   PART 4 : Convert Keras model (.h5) to TFLite model (.tflite)' -ForegroundColor "WHITE"
	Write-Host
	write-host "  Current folder : $car"
	write-host "  Command line : $command"
	Write-Host

	python $baseDonkeyPath\scripts\freeze_model.py --model=$car$modelsPath\$kerasmodel --output=$car$modelsPath\$tfmodel

	Write-Host
	Write-Host '  Conversion complete ! Review the logs for errors.' -ForegroundColor "GREEN"
	pause


	Logo
	
	$command = "python ""C:\Program Files (x86)\Intel\openvino_2021\deployment_tools\model_optimizer\mo_tf.py"" --input_model $car$modelsPath\$tfmodel --output_dir $car$modelsPath --model_name $model-optim --data_type FP32 --batch 1"

	Write-Host "  Optimizing model with OpenVINO..." -ForegroundColor "GREEN"
	Write-host ' ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄' -ForegroundColor "GREEN"
	Write-Host
	Write-Host '   PART 1 : Train to Keras model (.h5)' -ForegroundColor "GRAY"
	Write-Host '   PART 2 : Convert Keras model (.h5) to Tensorflow model (.pb)' -ForegroundColor "GRAY"
	Write-Host ' > PART 3 : Model optimization to use OpenVINO' -ForegroundColor "BLUE"
	Write-Host '   PART 4 : Convert Keras model (.h5) to TFLite model (.tflite)' -ForegroundColor "WHITE"
	Write-Host
	write-host "  Current folder : $car"
	write-host "  Command line : $command"
	Write-Host

	python "C:\Program Files (x86)\Intel\openvino_2021\deployment_tools\model_optimizer\mo_tf.py" --input_model $car$modelsPath\$tfmodel --output_dir $car$modelsPath --model_name $model-optim --data_type FP32 --batch 1

	Write-Host
	Write-Host '  Optimization complete ! Review the logs for errors.' -ForegroundColor "GREEN"
	pause


	Logo
	
	$command = "python $baseDonkeyPath\scripts\tflite_convert.py --model=$car$modelsPath\$kerasmodel --out=$car$modelsPath\$tflitemodel"

	Write-Host "  Converting Keras model (.h5) to TFLite model (.tflite)..." -ForegroundColor "GREEN"
	Write-host ' ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄' -ForegroundColor "GREEN"
	Write-Host
	Write-Host '   PART 1 : Train to Keras model (.h5)' -ForegroundColor "GRAY"
	Write-Host '   PART 2 : Convert Keras model (.h5) to Tensorflow model (.pb)' -ForegroundColor "WHITE"
	Write-Host '   PART 3 : Model optimization to use OpenVINO' -ForegroundColor "WHITE"
	Write-Host ' > PART 4 : Convert Keras model (.h5) to TFLite model (.tflite)' -ForegroundColor "BLUE"
	Write-Host
	write-host "  Current folder : $car"
	write-host "  Command line : $command"
	Write-Host

	python $baseDonkeyPath\scripts\tflite_convert.py --model=$car$modelsPath\$kerasmodel --out=$car$modelsPath\$tflitemodel

	Write-Host
	Write-Host '  Conversion complete ! Review the logs for errors.' -ForegroundColor "GREEN"
	pause
}


Function Start-Simulator
{
	$car = Select-car
	$command = "python manage.py drive"
	
	Logo
	
	Write-Host "  Starting Donkey Car in driving mode with simulator..." -ForegroundColor "GREEN"
	Write-host ' ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄' -ForegroundColor "GREEN"
	Write-Host
	write-host "  Current folder : $car"
	write-host "  Command line : $command"
	Write-Host

	Set-Location $car
	write-host "  Launching browser..."
	Start-Process powershell -argumentlist "-windowStyle hidden -command start-sleep -sec 12 ; start-process http://localhost:8887" # Waiting for donkey to start, and then launch a browser.
	Write-Host
	python manage.py drive
	
	Pause
}

Function Start-Simulator-Auto
{
	$car = Select-car
	$model = Select-model

	Logo

	$modeltype =""
	if ($model -like "*.tflite")
	{
		$modeltype = "--type=tflite_linear"
	}
	$command = "python manage.py drive --model=$model $modeltype"	
	
	Write-Host "  Starting Donkey Car in autopilot mode with simulator..." -ForegroundColor "GREEN"
	Write-host ' ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄' -ForegroundColor "GREEN"
	Write-Host
	write-host "  Current folder : $car"
	write-host "  Command line : $command"
	Write-Host

	Set-Location $car
	write-host "  Launching browser..."
	Start-Process powershell -argumentlist "-windowStyle hidden -command start-sleep -sec 16 ; start-process http://localhost:8887" # Waiting for donkey to start, and then launch a browser.
	Write-Host
	&python manage.py drive --model=$model $modeltype
	
	Pause
}

Function Update-Car
{
	$car = Select-car
	

	$command = "donkey update"
	
	Logo
	
	Write-Host "  Updating car from donkey car package..." -ForegroundColor "GREEN"
	Write-host ' ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄' -ForegroundColor "GREEN"
	Write-Host
	write-host "  Current folder : $car"
	write-host "  Command line : $command"
	Write-Host

	Set-Location $car
	donkey update
	
	Pause
}


Function Make-Movie
{

	Logo
	
	Write-Host "  Making a movie from data and model..." -ForegroundColor "GREEN"
	Write-host ' ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄' -ForegroundColor "GREEN"
	Write-Host
	Write-Host
	Write-Host "   Note : "
	Write-Host "       This option creates a movie using recorded images from previous sessions, and inject various models data :"
	Write-Host "        - Driver input (in green)"
	Write-Host "        - Model input (in blue)"
	Write-Host "        - Salient info (pixels which are used to trigger the neural network)"
	Write-Host
	Write-Host "       Due to a lack of compatibility between TensorFlow 2+ and Keras-Vis, a file outside of DK project must be modified :"  -ForegroundColor "RED"
	Write-Host "        In (env path)\donkey\Lib\site-packages\vis\backend\tensorflow_backend.py :"
	Write-Host "        Replace ""import tensorflow as tf"""
	Write-Host "             by ""import tensorflow.compat.v1 as tf"""
	Write-Host
	Pause

	$car = Select-car
	$model = Select-model
	$data = Select-data ($false)

	$modelBaseName = (Get-ChildItem $model).BaseName
	
	$command = "donkey makemovie --tub=$data --out=tubdata-movie-$modelBaseName.mp4 --model=$model --type=linear --salient"

	Logo
	Write-Host "  Making a movie from data and model..." -ForegroundColor "GREEN"
	Write-host ' ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄' -ForegroundColor "GREEN"
	Write-Host
	write-host "  Current folder : $car"
	write-host "  Command line : $command"
	Write-Host

	Set-Location $car
	Write-Host
	&donkey makemovie --tub=$data --out=tubdata-movie-$modelBaseName.mp4 --model=$model --type=linear --salient
	&tubdata-movie-$modelBaseName.mp4

	Pause
}


Function Stats
{

	Logo
	
	Write-Host "  Current software versions : " -ForegroundColor "GREEN"
	Write-host ' ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄' -ForegroundColor "GREEN"
	Write-Host
	Write-Host "OS VERSION : "
	Write-Host (Get-WmiObject -class Win32_OperatingSystem).Caption
	Write-Host
	Write-Host "PYTHON VERSION : "
	python --version
	Write-Host
	Write-Host "MAIN PIP MODULES :"
	
	pip list | findstr 'donkeycar tensorflow opencv gym-donkeycar openvino'

	Pause
}



Function Git-tools
{
	Logo

	Set-Location $baseDonkeyPath
	$branch = git branch
	$remoteRepo = git config --get remote.origin.url
	
	Write-host ' ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄' -ForegroundColor "GREEN"
	Write-Host
	Write-Host " Local folder : $baseDonkeyPath"
	Write-Host " Remote repository : $remoteRepo"
	Write-Host " Current branch : $branch"
	Write-Host
	Write-Host " Choose a GIT operation :"
	Write-Host
	Write-Host "  1) PULL remote updates from repository"
	Write-Host "  2) PUSH local updates to repository"
	Write-Host
	Write-Host "  0) Back"
	Write-Host
	Write-host ' ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄' -ForegroundColor "GREEN"

	$choice = Read-Host
	switch ($choice)
	{
		'1' {
			Logo 

			Write-Host "  Pulling remote updates to repository : " -ForegroundColor "GREEN"
			Write-host ' ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄' -ForegroundColor "GREEN"
			Write-Host
			Write-Host " Local folder : $baseDonkeyPath"
			Write-Host " Remote repository : $remoteRepo"
			Write-Host " Current branch : $branch"
			Write-Host

			git pull

			pause
		} '2' {
			Logo 

			Write-Host "  Pushing local updates to repository : " -ForegroundColor "GREEN"
			Write-host ' ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄' -ForegroundColor "GREEN"
			Write-Host
			Write-Host " Local folder : $baseDonkeyPath" 
			Write-Host " Remote repository : $remoteRepo"
			Write-Host " Current branch : $branch"
			Write-Host

			$commitMessage = Read-Host "Commit message "
			git add *
			git commit -m $commitMessage
			git push

			pause
		} '0' {
		}
	}
}


# MAIN :
# -----------------------------------------------------------------------------

Write-Host 
Write-Host "Testing donkey env..."
$result = pip list | findstr 'donkeycar'
if ($result -eq $null)
{
	Write-Host "Not in donkey env. Run conda activate donkey first !" -ForegroundColor "RED"
	Break
}
Write-Host "Done."

#Disabling TensorFlow 1.x verbose input
$Env:TF_CPP_MIN_LOG_LEVEL = "3"

mainmenu