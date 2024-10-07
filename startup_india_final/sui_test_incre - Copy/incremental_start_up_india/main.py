import sys
from config import startup_india_config
from functions import log, check_increment_data



def main():
    print("main function is called")
    if startup_india_config.source_status == "Active":
        # check_increment_data.check_increment_data(r"C:\Users\magudapathy.7409\Desktop\sui_test_incre\incremental_start_up_india\data\excel_sheet\new.xlsx")
        check_increment_data.check_increment_data(r"C:\Users\Premkumar.8265\Desktop\sui_test_incre - Copy\incremental_start_up_india\data\excel_sheet\final_excels_2024-10-04.xlsx")


        print("finished")

    elif startup_india_config.source_status == "Hibernated":
        startup_india_config.log_list[1] = "not run"
        log.insert_log_into_table(startup_india_config.log_list)
        startup_india_config.log_list = [None] * 4
        sys.exit("source is Hibernated")   

    elif startup_india_config.source_status == "Inactive":
        startup_india_config.log_list[1] = "not run"
        log.insert_log_into_table(startup_india_config.log_list)
        startup_india_config.log_list = [None] * 4
        sys.exit("source is Inactive")

if __name__ == "__main__":                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     
    main()
 