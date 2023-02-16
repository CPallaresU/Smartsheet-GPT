import smartsheet
from pyChatGPT import ChatGPT
import time


column_map = {}

# Helper function to find cell in a row
def get_cell_by_column_name(row, column_name):
    column_id = column_map[column_name]
    return row.get_column(column_id)

def evaluate_row_and_build_updates(source_row):
    # Find the cell and value we want to evaluate
    request_cell = get_cell_by_column_name(source_row, "Request")
    request_value = request_cell.display_value

    response_cell = get_cell_by_column_name(source_row, "Response")
    response_value = response_cell.display_value

    if request_value != None and response_value == None:
        gpt_prompt = api.send_message(request_value)  # ChatGPT Prompt
        gpt_response=gpt_prompt['message'] # ChatGPT Response

        # Build new cell value
        new_cell = smart.models.Cell()
        new_cell.column_id = column_map["Response"]
        new_cell.value = gpt_response

        # Build the row to update
        new_row = smart.models.Row()
        new_row.id = source_row.id
        new_row.cells.append(new_cell)

        print("################")
        print(new_row)
        return new_row
    

count=0

while True:
    ######## Auth for Smartsheet and ChatGPT ########

    chatgpt_token = "eyJhbGciOiJkaXIiLCJlbmMiOiJBMjU2R0NNIn0..VX_YnsRP2IxPlf2H.TMlwolGnLeHS4SHpYMLPe__3c5zKYluwr6ujiHCc6o7611AM-eS9Xvh_zSa7Tk6jvGhLbRsT1tD6A_38vpacl5m5H5KiPvXeW6rl5Pxz2Ts4lMPwl_N87RynEBmu3EogH2oA9QLvgjtpv03LT3mDHc0BrtMFNJ1_Sz8dxuD5U93ZdL8_daCYgPRzTlYnbx_bk5dH0nkBfoMW2Xt_-9hvJ14ds7i9kFfaBBxx_Pvup69fmTklwaxhumLIcEx-TU4oRylNW-7wnPCqwGKIPpuUQyvDFYFS1RsUV63k_RHA5NjKtrgqs86lSdCViUKHYaoxou3tvHvbepbfO32uqll2W61h-1SJGcDA9_GrscKJkQVkEZXO8rgdNO8L3nZMOS-G8igDI0qsn4INk4emRxCIU-Bpk3sQCoRv8f9862w8c_qz261P9A4R4T-7vbPQ-TqlcjbedZcowWB1QPS9QXVEdCHfphKIi7pWXisLU0rlZp0L3YzFC4HpFdmbgdZOjrilFVIbC31trJz8ufUaqfPTPUo8An_tz30KIzVzHAl6W2J50mvxnLh-Y1CxImaT2674uXPfl_bMl6GXEhEIkT9E5cnSs3bOjmvo87UPvEfA6Rxn16lZ8ryFpdXgerrbOZYXegLHIQgd7-69E4_3APgFaSu3TKIm2jgtyvk5Udhr0kLVZl4MsERQTyJW3dWFPxYGZO4xYOr0PYwfYMy3pjih13gcVv5xWhFcOhZgo7CrIBbnK-B_Kx-NwxGREdTQ4BJs4rMfosC_iZRv1q1XgRwyWWuUDOzCQkS2yCeiq69odmTktpCVfrTQ-kItsWfgBt2JCD8B-AAYX4YnhzwFA8vkoPAV-6m9j82yPXG_kGk2HPVCzbtpOC6J4C91GqNx7aVbVcpLSgVI35cRkb7szP8lBKGf-SplfVWB3owLQdAMF7h8T-7aOqiCFOduMBZpnoeRLZaovYDHkrqV5STacNKe_f73Yy4EJX4Kq_d_n39SekkIVwKFL4HyYwvoQfuEQwY3hvXZZFnSBXN3N_F1FT4CQnmpi5fr7Zc44U_Id27uqtaDj_JHjToG26pbwybyxtDB9yPOdYfDj2TVyqymmOOZcoeESrRLYQSQRvBCj5218QX7wZMkX3W1WS0i-IXBWC1IRVphByV9xKSyJUisY813zIgXsz5LzOrnaidI2f1skdnmn_cx2E-2iv0JsPjzDo7-TIERfakcyuytstqX1cbryel3VO0_eA3jC9t1bcC-WRPZhAI-80NJR6taoJ5kO16xzzWcFmiqdf5B1G_v8-vnOh5xmjYl07W4TH2SwTmr4k_GJLhFcsCiIgwTUHtsRUk_TXGOWRLBaTHDhiRUyV1oS3nq_VXFfiIuORKKGn2MyxL8ashVVp7jNQTmt041qSIpTYGQL21j8Y2IxJRIgbW1-5x-_US5LvU8vkXXZzadhZC2nQVF9nEar8hPK90G5eLIOftYDH7fuGCd6TZyvfsA8m9cH6Rp-d76Nl5Tcdz8vKN21hKCmRErwXn01A54dIWmu8RIzBbnNVB5vh7XxwB5yCGyukXDYbZ73i2zHnogYz25PiE2M5tKJEnbjeVPj-eypfmjJvlKu_h3TH-tnxU9VE1SwOye7jvN_WUpQavA1R3v2AsUqPtVgUNx3rT_VuxrO1fLkXOcM-0-gEeou7g41N4dl0XlPO2V1-IjMQ_bzYekv37HJgi38aMi-r55sKlIc3UbaARYjASMPO3QsjjvsD627PDFo6kDzQn95zucK9g3cyjQ6WGcmue1oOcEklYbKOLjlC1_LQTwpWMLSSNcKSXnSApzTP7hbaDZ4W0fu2wKfr-VdhLpaPA6b4849pCTDms3I4kgRYmVNyFu5mMK_F0qQGBqR3EJBU6p0yb0U14w3F5yG_YhssDtaG63vZ0hN9iXTiU6VdEALqOAsoPONa-dvCnubxUd3eD6RwVEm9_Wwq00FKS_d7R1JV39yvr7yuTrFlOq4Ia-n1BB8ZT7I-z_OMUibr5XuKz_ksitUDQmoKnhqcL0Y7foyVQMWo2OMOwfuGhccUwZH6sQi275j7YbNSOQPyK4ZYXaeELcHQWCbFt8hzVnv9Y4zSJvZ3aVxM-rHAkL-s1O_wh4rbbh5lE3DfSAqp9KSUw3aULEmehtwouwPvizZxcI1m8_SJ6hSFSzeUxovlM8_ZbbPxl1SN52spXS2lJPeOfy8MnT8b2ONeY044PIwJmbJK9h0ePniXYA-T_RvZbWvPkcwOY9LcCpbQijm-juGf8SjVYN_5HzUEchTiYKSfDJdmRODfbfVpb2-6PYryMimQgFl9LMN8rPYQuCUsOZKFtwlOaNhQ7n6zjYXGzOTO7AifLSHNG3n8nRqRGRIiSG4w0zAs45SuSMt82yFsQOeym2XumDx8Cx6aubTrAsDJSRVf0ZvZjzXPChZfvDlJQp_SKLJXgo6KK3MHjAvzXEbcxJsyV1gSQpsuEboLW-EM65rRlTi98WOO6sAeLp5HYoOI4Tbpn5hzkzjCJEP9JS6gFqGdakwoK6Z0lukzgKxck7ZfDFiMrrow.mQkHVvt_32UueMT3XeLrUg"
    api=ChatGPT(chatgpt_token)

    smart = smartsheet.Smartsheet("RJwq7hX5mKtd5qS9yEtmRXbCauzkTVza3uyV7")             # Create a Smartsheet client 

    response = smart.Sheets.list_sheets()       # Call the list_sheets() function and store the response object
    sheetId = response.data[0].id               # Get the ID of the first sheet in the response
    sheet = smart.Sheets.get_sheet(4650849919100804)     # Load the sheet by using its ID

    ######## Auth for Smartsheet and ChatGPT ########

    for column in sheet.columns:
        column_map[column.title] = column.id

    rowsToUpdate = []

    for row in sheet.rows:
        print(row)
        rowToUpdate = evaluate_row_and_build_updates(row)
        if rowToUpdate is not None:
            rowsToUpdate.append(rowToUpdate)

    # Finally, write updated cells back to Smartsheet
    if rowsToUpdate:
        print("Writing " + str(len(rowsToUpdate)) + " rows back to sheet id " + str(sheet.id))
        result = smart.Sheets.update_rows(4650849919100804, rowsToUpdate)
    else:
        print("No updates required")
    count+=1
    api.reset_conversation()
    time.sleep(20)
    print("Cycle: #"+str(count))

    break




