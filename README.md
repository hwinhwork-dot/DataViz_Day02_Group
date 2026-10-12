# Data Visualization, Day 02: Group Work

My group keeps all of its Session 2 work for the Data Visualization course in this repository. The work has two parts. The first part is four short activities (A to D) from the Session 2 slides. The second part is Group Homework 2, where my group answers four questions about the 2025 orders of a made-up grocery delivery service called GoMart.

Team name: not chosen yet.

## Members and branches

Each member works on their own branch.

| Member | Branch |
|---|---|
| Nguyễn Hoàng Minh (leader) | `hwinh` |
| Phạm Quang Minh | `quang-minh` |
| Phạm Tuấn Anh | `tuan-anh` |
| Trần Nhã Đoan | `nha-doan` |
| Nguyễn Minh Nguyệt | `minh-nguyet` |
| Trần Nguyễn Thanh Thảo | `thao` |

## How my group works together

A member never pushes to `dev` or `main` directly. A member pushes to their own branch and then opens a pull request into `dev`. The leader reads the pull request and merges it. When my group is ready to hand in the work, the leader opens a pull request from `dev` into `main`.

GitHub enforces these rules for us:

- The `main` branch accepts pull requests only from `dev`, and only the repository owner can merge them.
- The `dev` branch accepts changes only through pull requests, and only the repository owner can merge them.
- A pull request into `main` from any other branch fails the check named `chi-nhan-tu-dev`. A pull request into `main` that a member opens is also closed automatically.
- Nobody can delete a member branch.

### Steps for a member

First, download the repository and switch to your own branch. The example below uses the branch `thao`.

```bash
git clone https://github.com/hwinhwork-dot/DataViz_Day02_Group.git
cd DataViz_Day02_Group
git checkout thao
```

Before you start working, pull the newest work from `dev`.

```bash
git pull origin dev
```

When you finish a piece of work, save it and push it to your own branch.

```bash
git add .
git commit -m "Short description of the change"
git push origin thao
```

Last, open GitHub, go to Pull requests, and choose New pull request. Set the base branch to `dev` and the compare branch to your own branch.

## Folders

```
.
├── activities/       Activities A to D, one Python file for each, plus one file that runs all four
├── homework/         Group Homework 2 (notebook, clean data, images, notes)
├── data/
│   ├── raw/          The original data files, which we never edit
│   └── processed/    Empty for now
├── notebooks/        Empty for now
├── src/              Shared Python code (style.py gives every activity chart the same look)
├── outputs/
│   └── figures/      The four activity images
├── reports/          Empty for now
└── requirements.txt
```

## Setup

The commands below create a virtual environment and install the packages.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
jupyter lab
```

## Activities A to D

Each activity is a separate Python file. When you run it, it saves one image into `outputs/figures/`. The data comes from the course, and all of it is simulated.

- Activity A asks which type each of six datasets is. My group found that only the delivery orders that arrive right now form a stream. Two other items can be argued in two ways. See [the code](activities/activity_a_dataset_types.py) and [the image](outputs/figures/activity_a_dataset_types.png).
- Activity B sorts the eleven columns of an online shop table into categorical, ordinal and quantitative types. Only `order_id` is a key, and my group should never average `order_id`. See [the code](activities/activity_b_attribute_types.py) and [the image](outputs/figures/activity_b_attribute_types.png).
- Activity C turns a wide table into a long table with `melt`. The result has six rows, and the keys are the branch and the category. My group also shows why a new date is one extra column in the long table but three extra columns per day in the wide table. See [the code](activities/activity_c_reshape.py) and [the image](outputs/figures/activity_c_reshape.png).
- Activity D rewrites four vague requests as clear tasks and answers each one with a chart that my group drew from the real data. See [the code](activities/activity_d_vague_to_precise.py) and [the image](outputs/figures/activity_d_vague_to_precise.png).

To run all four at once, use the first command below. To run one activity, use the second command.

```bash
python activities/run_all_activities.py
python activities/activity_c_reshape.py
```

The charts follow the style of our Session 1 work. They use a serif font, black and grey ink, one accent colour, a title that states the finding, and a source line at the bottom. My group also checked the colours with a colour-blindness test.

## Group Homework 2: GoMart deliveries

My group has finished all eight tasks of Group Homework 2. The notebook that we hand in is [GH2_TeamName.ipynb](homework/gh2_gomart/GH2_TeamName.ipynb). The cleaned data is in [gomart_orders_clean.csv](homework/gh2_gomart/gomart_orders_clean.csv), and one image for each question is in [homework/gh2_visuals](homework/gh2_visuals/). The file [homework/README.md](homework/README.md) explains the details.
