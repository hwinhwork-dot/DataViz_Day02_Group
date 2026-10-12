# Data Visualization: Group Homework 2

My group keeps its work for Group Homework 2 of the Data Visualization course in this repository. In this homework, my group answers four questions about the 2025 orders of a made-up grocery delivery service called GoMart. The data is simulated.

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
├── homework/         Group Homework 2: the notebook, the clean data, the images and the notes
├── data/
│   └── raw/          The two original GoMart files, which we never edit
├── requirements.txt  The Python packages that we use
└── (empty folders)   data/processed, notebooks, outputs/figures, reports and src come from the course template
```

## Setup

The commands below create a virtual environment and install the packages.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
jupyter lab
```

## Group Homework 2: GoMart deliveries

My group has finished all eight tasks of Group Homework 2. The notebook that we hand in is [GH2_TeamName.ipynb](homework/gh2_gomart/GH2_TeamName.ipynb). The cleaned data is in [gomart_orders_clean.csv](homework/gh2_gomart/gomart_orders_clean.csv), and one image for each question is in [homework/gh2_visuals](homework/gh2_visuals/). The file [homework/README.md](homework/README.md) explains the details.
