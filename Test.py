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

    chatgpt_token = "eyJhbGciOiJkaXIiLCJlbmMiOiJBMjU2R0NNIn0..QdhI6ka5YozD27yO.1M6dmZHuf1OPusXlv2vklp7p-1_ZxFhZRgXaqoz9dgdBZq712ixdDNwJA3n1cDzhA1YnKTz3ujY7Om58MN2PpqCUGbPrXTZ5rZJ1N_ThMcn8aIvQV2ZUMkZ4UpxAnuHZnQ1u5-MIebpa5BFZP3MRrcSM-EE2ErzQzLLC1nJNCLkjgKvN3EU7Vrkp66AyU6agyVYISivGru6nvy4w0qSTAyjtqYEuNoTlvOxTbzI5Xq3xCIMWGq65co8OCIe5vtpDQjUO3oOxO5s3mNnn_qOf59ucWoWTTwbnQfDmBQeEMoQbiVowoxObKfwH3MGFpcLXFyTyttb-T3BAZ-cVE2xYP2DA9vpMbhpFojdTeor34JH-IzAy1WFNQN6ly7CLxdV2oDC1dcq7ByagiOQz0cdsegjLmKHfRNz7tWw7-wdGWm9_2ifO_LP3LQ6aeqsmBLRjAsPh-gveQ7U9mQFsi4l0XYploK2YT_5S-jSfZufau02AEb6RnEfBUN8q8vPFtSvgu0_SqxjEEyg_-3UkIX2OgWnyX3BuBEwD1xjuW2PV47HGugsyZ2NGd7mPbl32U0nFAbb0q7GY66UkzEuFSdSczDDgZT2Ut2mPPTNBpSeujfO8o4oHGbE8IWaHAcV_R3vuXTMnwiQ-EI8VmWjVhjJOsVNQ-Ey5rY4cqpZvZDI1LPt81PtLsmoePt8UHIAULrP_iOL9pxKs0Nn_RGMkA3ccWzptSl9tgQ5ohLqmTA4BT2P34-WQbu4pEoWkLacItQAVQYk5D7FGflb0bn0X1XaMJJ39KAUqm5Q2bVzH4q4RFfLz7CqCemrfdq4_bklQAEHZZ64HwqB4FYhjO75PIfrfUsH6bjyp7H6LK6UouVNSQbyqcRQpVYhD-kpbF4Xji2AY_ywr8yYs_qhwreMpFlp6MH2H-cZTQv0ArPudYFwCJrubFyiVcrIKK1zWN9Z15JkEAcRE6sY3HV7SzlE6Cy6a-RfbYMkSRBsl3I8lMf_DUFebK6sxUCKT8mwLsdfnuOKsK4uP-1Vfa9QkAVt4OMGTu--Sw6ANBG_jUJkCPF-rXNUpATsVBXPQQC5AvluEHUz2WE2ZZfpmzopnWgDCUmIiJKFVuHypMp7EOf8f4fXtzB6vfke6g_-7Qc-D3GZEfAbApKzd77rZlhI7Yzivg4aSGsBYJyUzKY8lJ-SFeAx4Np-2e89H__RmLzm3_ZwwaRr0IlANbKrmef0YJUuLbOR9gsZP53AxO0p7jSUj2-IJSIcIc8sL32DpeTDPJByBjkNH4dTcah4cw3wnpFcQwrkxteEGmP5ZusEnwDORc9cs2k1f3Fs8oxLuMM93blJQpMLmCDSU_tB6bBseTvDT1Z8OtsqC__SBp1WIbe7qqCwmvXZKpMC4TEJlEdFnMR2AY6v5WsM35rphYoI6Q0-29L1M56lSnwyJ65Up-f-8Tyz-dKqCFM1W_LBcA_SvW6qNvBBbEjn_jsoNMxpS6StJDBwRow0GB4q3EDYIBC39DdfgTHgpaAckX1BuwPOr26ixrBFqjz-28uOYlrsWS18NCyYDS7oo0Nm5Duhk1GkY30iqZ7oTqmzAKiyozD5vRf1jSMQb66d_QcFzLdSy4CYfZ6LlfLPPSCHXHsXLCj6wvsVmkLzeDBvD9XGirKRlIak2mOgkRd36qgOPOKbbEWt0hijIA4kLO6CKojxH6q-SSD1YGKVvBAJrGXSNMZLn0LRoF9x3p0Z3pXrK7hkRVY-qz5tcd8irvBOdwW71RCd2zXPPDG75yHSHWI9GBtIAvzwS5ZWQYCM--kyzeu6HY-nT0dW3lftfgFDKE90VV8GDpN6Nx8aXom2Fms7gn6eksGn74uJ2Wx2XpjGhbWyEMZJVpWcfL-cWQIHQZNcqvCwOn0xLnx9F3zMzPCT6fWVa6E8VSIN2DDmVt2mtXz52ncmCVPUpy1Q-zvEdBuP43hiRtFIe7ZH_5kkt6QSt2PZzvsChqTZYWUxPhxMhEEUVPXxt_ykojxoi84DoL9BfeuSDnQn-8THaLfydWO5CGxR8ppIz3j_HgKj8YMN_hk4AQoYQTuIujWX-zbOBfVnVzXk-aso9glQLYzwRq9gaoQbxZO06U8HMcQ6ePQCADSB2KhfRCtGmvh2CB5KR2n0RNMQ4CE4y88czAHNFyk1KEq6QUnnAl4wqSWXgijpZ9xKo2cckiAsHhZVTdz_7FUqOS3YTZs0mRbA1pmdHZtWQfLUMIjRzBjOvsQyL8UWSPebCGBVoMsXk4udebpZeXx_TAwS-7KaOHQfLXlLzAjYrtWv1Wf0c8nCWPlyERnkj4B_ZwgGtePSswgKhsNQppS8jURfyPJaj8bOdp79CmQs0OcEvycj8-n0ppPu8pOGDxOXgt9RkInn7IwC1wKRUW0UviP7o0Xv_VTyvwo6RjRj_W-LnzLuY-ss4y0nWRAaH1riFYj45UctZrT_6qplAuGu7pPUmKWmwvgfmf98fyTX6Bo9njMnYpijGD3chkfxQqCd8UGt6bQC-6XYuFNgN4bUTmq369Xle-jKpg1vh9r6A4CqBiHmhZ3R5pQ.XMuUG1nd8ekKiS53ZaQurQ"

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




