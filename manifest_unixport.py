freeze_as_mpy('$(MPY_DIR)/tools', 'upip.py')
freeze_as_mpy('$(MPY_DIR)/tools', 'upip_utarfile.py', opt=3)
freeze('usermods/udisplay_f469/display_unixport')
freeze('libs')