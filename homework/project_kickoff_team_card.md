# Project kick-off: team card (Session 2, slide 58)

This card is also Task 0 of Group Homework 2, and the copy inside the notebook is the one that my group hands in. The next milestone is a one-page proposal in Session 4, which names a dataset and its questions. The three datasets below are my group's draft ideas, and we can still change them.

Team name: not chosen yet.

## Members

| Student ID | Name | Role |
|---|---|---|
| 31221020403 | Phạm Tuấn Anh | |
| 31241027205 | Trần Nhã Đoan | |
| 31221021575 | Nguyễn Hoàng Minh | Leader |
| 31221021576 | Phạm Quang Minh | |
| 31241021154 | Nguyễn Minh Nguyệt | |
| 31241026554 | Trần Nguyễn Thanh Thảo | |

The brief asks for teams of three or four students, and my group has six members, so we still have to ask the lecturer about this.

## Three candidate datasets

Before my group picks a dataset, we check that we can name its keys, its values and the type of every attribute. If we cannot do that, we choose another dataset.

### Dataset 1: World Development Indicators (World Bank Open Data)

Source: <https://data.worldbank.org/indicator/IT.NET.USER.ZS>

| | |
|---|---|
| Dataset type | A multidimensional table, static |
| Keys | Country and year |
| Main values | Internet users as a share of the population, and GDP per capita. Both are quantitative and sequential. |
| Question 1 | *Summarize* the *trend* of internet use in Viet Nam and its ASEAN neighbours from 2000 to 2024. |
| Question 2 | *Discover* the *correlation* between GDP per capita and internet use across ASEAN countries. |

### Dataset 2: Brazilian E-Commerce Public Dataset by Olist (Kaggle)

Source: <https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce>

| | |
|---|---|
| Dataset type | Several flat tables that are linked by keys, static, with about 99,000 orders from 2016 to 2018 |
| Keys | `order_id` and `customer_id` |
| Main values | The delivery dates are quantitative, the review score from 1 to 5 is ordinal, and the customer state is categorical. |
| Question 1 | *Discover* the *dependency* of the review score on late delivery. |
| Question 2 | *Compare* the *distribution* of delivery time across customer states. |

This dataset is close to the GoMart data, so my group can use the same cleaning and charting skills again.

### Dataset 3: Provincial statistics of Viet Nam (National Statistics Office, formerly GSO)

Source: <https://www.nso.gov.vn>

| | |
|---|---|
| Dataset type | A multidimensional table, static. It can be joined to province borders (geometry) to draw a map. |
| Keys | Province and year |
| Main values | Population and monthly income per person are quantitative, and the region is categorical. |
| Question 1 | *Compare* the *extremes* of income per person across provinces. |
| Question 2 | *Summarize* the *trend* of income by region. |

The provinces were merged in 2025, so different tables may use different lists of provinces. My group must check this before we join several years.

## How to write a question

A good question has an action and a target. For example, "*Compare* the *extremes* of revenue across branches" is a good question. A request such as "Show sales" is not a good question, because it has no action and no target.
