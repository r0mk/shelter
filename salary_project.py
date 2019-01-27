#!/usr/bin/python3
#Install: pip3 install openpyxl 
import sys
from openpyxl import load_workbook
from openpyxl.utils import get_column_letter
import datetime
#wb2 = load_workbook('schedule.xlsx',data_only = True)
if len(sys.argv) < 2:
    print('Usage ./script file.xlsx')
    sys.exit()
try:
    wb2 = load_workbook(sys.argv[1],data_only = True)
except:
    print('File {} not found'.format(sys.argv[1]))

sheet_ranges = wb2[wb2.sheetnames[0]]
#print(wb2.sheetnames)
rows = sheet_ranges.iter_rows(min_row=1, max_row=1)
employee_id = sheet_ranges.iter_cols(min_col=1, max_col=1)
not_needed = ['Totals', 'Labor Cost', 'Actual Sales', 'Labor %',  'Unpaid Breaks', 'Hourly Rate', 'Total', 'Employee ID', 'Position']

first_row = next(rows)
#row_lenth = len(first_row)
for cell in first_row:
    if cell.value and cell.value not in not_needed:
        #print('column name ' + str(cell.value))
        #print(dir(cell.value))
        pass
year = sheet_ranges['D1'].value.year
month = sheet_ranges['D1'].value.month
print(year)
print(month)

first_col = next(employee_id)
col_lenth = len(first_col)

with open('Output.csv','w') as f:
    f.write('Loonjaar,Periode,Medewerker,Type,Salaris component,Invoer type,Waarde\n')

for cell in first_col:
    earned = []
    if cell.value and cell.value not in not_needed:
        #print('employee id ' + str(cell.value))
        #print('row number= ' + str(cell.row))
        earned = ([sheet_ranges['AI'][cell.row - 1].value])
        #print('begin ' + str(worked_hours))
        #print('check if empty ' + str(sheet_ranges['B' + str(cell.row)].value))
        for pos_counter in range(1,10):
            #print('next id exist on A' + str(cell.row + pos_counter) +  '?: ' + str(sheet_ranges['A' + str(cell.row + pos_counter)].value))
            #print(sheet_ranges['B' + str(cell.row + pos_counter)].value)
            if sheet_ranges['B' + str(cell.row + pos_counter)].value == None and sheet_ranges['A' + str(cell.row + pos_counter)].value == None:
                earned.append(sheet_ranges['AI'][cell.row + pos_counter - 1].value)
                #print(sheet_ranges['AI' + str(cell.row + pos_counter)].value)
                pos_counter = pos_counter + 1
                #print(pos_counter)
                #print(earned)
            else:
                #earned.append(sheet_ranges['AI'][cell.row + pos_counter - 1].value)
                #print('Continue with next employee\n\n')
                #print(earned)
                break
        worked_days = 0
        worked_hours = []
        for day in range(1,32):
            for position in range(0,pos_counter):
                #print(cell.col_idx)
                #print('Day ' +  str(sheet_ranges[get_column_letter(day + 3)][cell.row + pos_counter ].value))
                if sheet_ranges[get_column_letter(day + 3)][cell.row + position -1].value:
                    #print('column= ' + str(get_column_letter(day + 3 )))
                    #print(str(cell.value) + ' worked at ' + str(sheet_ranges[get_column_letter(day + 3 )][0].value) + ' day')
                    #print(str(cell.value) + ' worked time: ' + str(sheet_ranges[get_column_letter(day + 3 )][cell.row + position -1].value) + ' hours')
                    worked_days = worked_days + 1
                    worked_hours.append(sheet_ranges[get_column_letter(day + 3 )][cell.row + position -1].value)
                #print('pos_count ' + str(position))
                #print('work on day:' + str(sheet_ranges['AI'][cell.row + pos_counter ].value))
        try:
            print('{},{},{},1,,1,{}'.format(year,month,cell.value,worked_days))
            print('{},{},{},2,,1,{}'.format(year,month,cell.value,round(sum(worked_hours))))
            with open('Output.csv','a') as f:
                f.write('{},{},{},1,,1,{}\n'.format(year,month,cell.value,worked_days))
                f.write('{},{},{},2,,1,{}\n'.format(year,month,cell.value,round(sum(worked_hours))))

            #print('positions count: ' + str(pos_counter) + 'id:' + str(cell.value))
            #print('id: ' + str(cell.value) + 'work days ' + str(worked_days) + '  worked hours: ' + str(sum(worked_hours)))
            #print('positions count: ' + str(pos_counter) + ' Earned ' + str(sum(earned)) + '    id:' + str(cell.value))
            #print('id: ' + str(cell.value) +  '  Earned: ' + str(sum(earned.remove(None))) + '  work days: ' + str(worked_days.remove(None)) + '  worked hours: ' + str(sum(worked_hours.remove(None))))
        except:
            pass
        #sys.exit()
