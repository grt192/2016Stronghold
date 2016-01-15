class Robot(IterativeRobot):
	autonomousCommand = None
	autoChooser = None

	def __init__(self):
		self.autoChooser = SendableChooser()
		self.autoChooser.addDefault("Basic Auto", BasicAuto)
		self.autoChooser.addObject("One Bin Steal", OneBinSteal)
		self.autoChooser.addObject("Two Bin Steal", TwoBinSteal)
		self.autoChooser.addObject("Backup Bin Steal", BackupBinSteal)
		self.SmartDashboard.putData("Autonomous mode chooser", self.autoChooser)

	def autonomousInit(self):
		self.autonomousCommand = autoChooser.getSelected()
		self.autonomousCommand.start()

	def autonomousPeriodic(self):
		Scheduler.getInstance().run()

	

