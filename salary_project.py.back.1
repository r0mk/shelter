#!/usr/bin/python3
import sys
from openpyxl import load_workbook
from openpyxl.utils import get_column_letter
wb2 = load_workbook('schedule.xlsx',data_only = True)
sheet_ranges = wb2[wb2.sheetnames[0]]
print(wb2.sheetnames)
rows = sheet_ranges.iter_rows(min_row=1, max_row=1)
employee_id = sheet_ranges.iter_cols(min_col=1, max_col=1)
not_needed = ['Totals', 'Labor Cost', 'Actual Sales', 'Labor %',  'Unpaid Breaks', 'Hourly Rate', 'Total', 'Employee ID', 'Position']

first_row = next(rows)
row_lenth = len(first_row)
for cell in first_row:
    if cell.value and cell.value not in not_needed:
        print('row name ' + str(cell.value))

first_col = next(employee_id)
col_lenth = len(first_col)
for cell in first_col:
    earned = []
    if cell.value and cell.value not in not_needed:
        #print('employee id ' + str(cell.value))
        #print('row number= ' + str(cell.row))
        earned = ([sheet_ranges['AI'][cell.row - 1].value])
        #print('begin ' + str(worked_hours))
        for pos_counter in range(1,20):
            #print('next id exist on A' + str(cell.row + pos_counter) +  '?: ' + str(sheet_ranges['A' + str(cell.row + pos_counter)].value))
            if sheet_ranges['B' + str(cell.row + pos_counter)].value == None:
                earned.append(sheet_ranges['AI'][cell.row + pos_counter - 1].value)
                #print(sheet_ranges['AI' + str(cell.row + pos_counter)].value)
                pos_counter = pos_counter + 1
                pos_count = pos_counter
                #print(earned)
            else:
                print('Continue with next emp')
                break
        worked_days = 0
        worked_hours = []
        for day in range(1,32):
            for position in range(0,pos_count):
                #print(cell.col_idx)
                #print('Day ' +  str(sheet_ranges[get_column_letter(day + 3)][cell.row + pos_counter ].value))
                if sheet_ranges[get_column_letter(day + 3)][cell.row + position -1].value:
                    #print('column= ' + str(get_column_letter(day + 3 )))
                    print(str(cell.value) + ' worked at ' + str(sheet_ranges[get_column_letter(day + 3 )][0].value) + ' day')
                    print(str(cell.value) + ' worked time: ' + str(sheet_ranges[get_column_letter(day + 3 )][cell.row + position -1].value) + ' hours')
                    worked_days = worked_days + 1
                    worked_hours.append(sheet_ranges[get_column_letter(day + 3 )][cell.row + position -1].value)
                #print('pos_count ' + str(position))
                #print('work on day:' + str(sheet_ranges['AI'][cell.row + pos_counter ].value))
        try:
            print('positions count: ' + str(pos_count) + ' Earned ' + str(sum(earned)) + '    id:' + str(cell.value))
            print('id: ' + str(cell.value) +  '  Earned: ' + str(sum(earned)) + '  work days: ' + str(worked_days) + '  worked hours: ' + str(sum(worked_hours)))
        except:
            pass
        #sys.exit()

#if sheet_ranges['B' + str(cell.row)].value
#print(headings)
#headings = [c.value 
#print(headings)
#list_with_values = []
#for cell in sheet_ranges:
#  print((cell))
