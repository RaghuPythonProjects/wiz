from utilities.wiz_master import WizMaster


wiz_master = WizMaster()
#wiz_master.report_rerun()
report_run_status = wiz_master.report_status()
if report_run_status == 'COMPLETED':
    wiz_master.report_download_url()

