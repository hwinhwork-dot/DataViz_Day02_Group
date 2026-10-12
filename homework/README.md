# Group Homework 2: GoMart deliveries

This folder holds my group's answer to Group Homework 2. In this task, the operations manager of GoMart asks four questions about the orders of 2025. GoMart is a made-up online grocery service in Ho Chi Minh City, and all of its data is simulated. The notebook that my group hands in is `gh2_gomart/GH2_TeamName.ipynb`.

## What is in this folder

- `gh2_gomart/GH2_TeamName.ipynb` is the notebook that we hand in. It already holds the results of a full run, so you can see every chart when you open it.
- `gh2_gomart/gomart_orders_clean.csv` is the cleaned order table. The notebook creates it in Task 4. It has 5,913 orders, and each order has its zone, its distance to the hub, and the hour, weekday and month.
- `gh2_visuals/` holds one image for each question, and `export_visuals.py` creates the images again.
- `project_kickoff_team_card.md` is the draft of our three candidate datasets for the course project.

The raw data is in `data/raw/`, in the files `gomart_orders_2025.csv` and `gomart_districts.csv`.

## The four questions

| Question | Answered by | What my group found |
|---|---|---|
| Q1: Where are deliveries slow? | Quang Minh | Deliveries are slowest in the Outer zone, and every extra kilometre from the hub adds about 2.6 minutes. |
| Q2: Is the move to e-wallet payments real? | Thảo | The e-wallet share of orders grew from 31% in January to 60% in December. |
| Q3: Do slow deliveries cost good ratings? | Minh Nguyệt | Ratings stay high up to about 30 minutes, and then they fall quickly. |
| Q4: When are the order peaks? | Tuấn Anh | Orders peak at lunch time and even more in the evening, and 19:00 is the busiest hour. |

Hoàng Minh and Nhã Đoan worked together on Tasks 1 to 4, which are looking at the raw data, naming the columns, cleaning the file and joining the district table. My group wrote the memo in Task 6 with two Big Ideas, which are to move riders into the peak hours and to promote e-wallet payments. The team table and the AI log are in Task 7 of the notebook.

## How the notebook works

My group wrote the notebook so that it runs from the first cell to the last cell without any error. Here is what happens when you run it:

1. The memo chart at the top reads the raw file and cleans it in a short form, so it can run before Task 3.
2. Task 3 cleans the file with the function `clean_orders`, and it counts the rows that each step changes.
3. Task 4 joins the district table and saves `gomart_orders_clean.csv` next to the notebook.
4. Task 5 answers the four questions, one after the other.

Inside the repository, the notebook finds the data in `data/raw/`. In Google Colab, you first upload the two raw files next to the notebook. While it runs, the notebook may save a few extra images into an `outputs` folder, and git ignores that folder because the same charts are already inside the notebook.

## Images of the four questions

To create the images again, run the command below from the repository root.

```bash
python homework/gh2_visuals/export_visuals.py
```

The script runs the notebook in a temporary folder. It collects the charts of a question and puts them one under the other in a single image, so each question has exactly one image. It does not change any chart. For Q1, the image shows the two simple bar charts. The box plots and the scatter plot of Quang Minh come after a note that starts with "More detail", so the script stops collecting charts there and these charts stay in the notebook only. The script needs pandas, matplotlib, seaborn and pillow.

## What is still open

Before my group hands in the notebook, we still have to choose a team name. We will write the name into the first cell and into Task 0, and then we will put it into the file name, for example `GH2_OurTeamName.ipynb`.
