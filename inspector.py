from rich import print
from rich.panel import Panel
import sys


def read_dataset(file_path):
    dataset = []
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            dataset.append(line.strip().split(","))
    return dataset


def inspect_data(dataset):
    header = dataset[0]
    expected_count = len(header)
    rows = dataset[1:]
    errors_count = 0
    seen_ids = []
    broken_counts = 0
    
            
    for index, row in enumerate(rows, start = 1):

        row_has_error = False
        
        if len(row) != expected_count:
            print(f"[bold red][Row {index}] Schema Error: expected {expected_count} columns, got {len(row)}![/bold red]\n")
            errors_count += 1
            row_has_error = True
        else:
            email = row[3]
            name = row[1]
            age = row[2]
            for char in name:
                if char.isdigit():
                    print(f"[bold red][Row {index}] Name Error: digits found in name '{name}'![/bold red]\n")
                    errors_count += 1
                    row_has_error = True
                    break
            if "@" not in email or "." not in email:
                print(f"[bold red][Row {index}] Email Error: invalid format '{email}'![/bold red]\n")
                errors_count += 1
                row_has_error = True
            for position in age:
                if position.isalpha():
                    print(f"[bold red][Row {index}] Age Error: non-numeric characters in age '{age}'![/bold red]\n")
                    errors_count += 1
                    row_has_error = True
                    break
        
                
            
            
            
            
        if "" in row:
            print(f"[bold red][Row {index}] Null Value: empty field detected![/bold red]\n")
            errors_count += 1
            row_has_error = True
            
         
        if row[0] in seen_ids:
            print(f"[bold red][Row {index}] Duplicate Error: duplicate Primary ID '{row[0]}'! [/bold red]\n")
            errors_count += 1
            row_has_error = True
        else:
            seen_ids.append(row[0])
            
        if row_has_error:
            broken_counts += 1
    clean_rows_count = len(rows) - broken_counts
    purity_rate = (clean_rows_count / len(rows)) * 100
            
    if errors_count == 0:
        status = "[bold green]DATASET VERIFIED [OK][/bold green]"
        box_color = "green"
    else:
        status = "[bold red]REQUIRES CLEANING [!][/bold red]"
        box_color = "red"
    text_panel = (f'''
[dim]Total rows checked:[/dim]     {len(rows)}
[dim]Defects found:[/dim]          {errors_count}
[dim]Data Purity:[/dim]            {purity_rate:.1f}%
[dim]Status:[/dim]                 {status}''')
    print(Panel(text_panel, title ="[bold yellow]DIAGNOSTIC REPORT[/bold yellow]", border_style = box_color, expand = False))
    

def clear_data(dataset, output_path):
    header = dataset[0]
    clean_rows = []
    seen_ids = []
    rows = dataset[1:]
    for index, row in enumerate(rows, start =1):
        if len(row) == len(header) and "" not in row and row[0] not in seen_ids and row[1].isalpha() and row[2].isdigit() and "@" in row[3] and "." in row[3]:
            clean_rows.append(row)
            seen_ids.append(row[0])
                    
    with open(output_path, "w", encoding="utf-8") as file:
        file.write(",".join(header) + "\n")
        for row in clean_rows:
            file.write(",".join(row) + "\n")
            
        
        
    
    
try:
    if len(sys.argv) < 2:
        print(f'''[bold red]Error: Please provide path to CSV file![/bold red]
[dim]Example: py inspector.py dirty_data.csv[/dim]''')
        sys.exit()
    else:
        file_path = sys.argv[1]
        data = read_dataset(file_path)
        inspect_data(data)
        if "--clean" in sys.argv:
            clean_file_path = "clean_data.csv"
            clear_data(data, clean_file_path)
            print(f"[green]Dataset successfully sanitized and saved to '{clean_file_path}'![/green]")
except FileNotFoundError:
    print(f"[bold red]Error: File '{file_path}' not found on disk![/bold red]")


        