import json
import pickle

import numpy as np
import pandas as pd

from celery import task
from datetime import datetime
from sklearn import preprocessing
from sklearn import svm
from sklearn.ensemble import AdaBoostClassifier, VotingClassifier
from sklearn.model_selection import cross_val_score
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier

from ml.models import RecommendedData


dataset_filename = "data/dataset.csv"



def get_year(temp_date_str):
    if temp_date_str is not None and type(temp_date_str) is not float:
        try:
            return datetime.strptime(temp_date_str, '%Y-%m-%d').year
        except ValueError:
            return datetime.strptime(temp_date_str, '%Y-%m-%d %H:%M:%S').year
    else:
        return 2013
    pass


def get_month(temp_date_str):
    if temp_date_str is not None and type(temp_date_str) is not float:
        try:
            return datetime.strptime(temp_date_str, '%Y-%m-%d').month
        except ValueError:
            return datetime.strptime(temp_date_str, '%Y-%m-%d %H:%M:%S').month
    else:
        return 1
    pass


def prepare_data():
    temp_user_data_df = pd.read_csv(dataset_filename, sep=",", low_memory=False).dropna()
    temp_user_data_df = temp_user_data_df.sample(frac=0.001, random_state=99)

    temp_user_data_df['date_time_year'] = pd.Series(temp_user_data_df.date_time, index=temp_user_data_df.index)
    temp_user_data_df['date_time_month'] = pd.Series(temp_user_data_df.date_time, index=temp_user_data_df.index)
    temp_user_data_df.date_time_year = temp_user_data_df.date_time_year.apply(lambda date_str: get_year(date_str))
    temp_user_data_df.date_time_month = temp_user_data_df.date_time_month.apply(lambda date_str: get_month(date_str))
    del temp_user_data_df['date_time']

    temp_user_data_df['srch_ci_year'] = pd.Series(temp_user_data_df.srch_ci, index=temp_user_data_df.index)
    temp_user_data_df['srch_ci_month'] = pd.Series(temp_user_data_df.srch_ci, index=temp_user_data_df.index)
    temp_user_data_df.srch_ci_year = temp_user_data_df.srch_ci_year.apply(lambda date_str: get_year(date_str))
    temp_user_data_df.srch_ci_month = temp_user_data_df.srch_ci_month.apply(lambda date_str: get_month(date_str))
    del temp_user_data_df['srch_ci']

    temp_user_data_df['srch_co_year'] = pd.Series(temp_user_data_df.srch_co, index=temp_user_data_df.index)
    temp_user_data_df['srch_co_month'] = pd.Series(temp_user_data_df.srch_co, index=temp_user_data_df.index)
    temp_user_data_df.srch_co_year = temp_user_data_df.srch_co_year.apply(lambda date_str: get_year(date_str))
    temp_user_data_df.srch_co_month = temp_user_data_df.srch_co_month.apply(lambda date_str: get_month(date_str))
    del temp_user_data_df['srch_co']

    # temp_user_data_df = temp_user_data_df.loc[temp_user_data_df['is_booking'] == 1]

    return temp_user_data_df


def get_x_y_axis(temp_df):
    temp_x_axis = temp_df.drop(['srch_adults_cnt', 'srch_children_cnt', 'srch_rm_cnt', 'user_id',], axis=1)
    temp_y_axis = temp_df.hotel_id

    return temp_x_axis, temp_y_axis


def apply_naive_bayes(temp_x_axis, temp_y_axis):
    temp_naive_clf = make_pipeline(preprocessing.StandardScaler(), GaussianNB(priors=None))
    temp_naive_clf.fit(temp_x_axis, temp_y_axis)
    # np.mean(cross_val_score(temp_naive_clf, temp_x_axis, temp_y_axis, cv=5))

    return temp_naive_clf


def apply_k_neighbours(temp_x_axis, temp_y_axis):
    temp_k_neighbours_clf = make_pipeline(preprocessing.StandardScaler(), KNeighborsClassifier(n_neighbors=5))
    temp_k_neighbours_clf.fit(temp_x_axis, temp_y_axis)
    # np.mean(cross_val_score(temp_k_neighbours_clf, temp_x_axis, temp_y_axis, cv=5, scoring='accuracy'))

    return temp_k_neighbours_clf


def apply_decision_tree(temp_x_axis, temp_y_axis):
    temp_decision_tree_clf = make_pipeline(preprocessing.StandardScaler(), DecisionTreeClassifier())
    temp_decision_tree_clf.fit(temp_x_axis, temp_y_axis)

    return temp_decision_tree_clf


def apply_adaboost(temp_x_axis, temp_y_axis):
    temp_adaboost_clf = make_pipeline(preprocessing.StandardScaler(), AdaBoostClassifier())
    temp_adaboost_clf.fit(temp_x_axis, temp_y_axis)

    return temp_adaboost_clf


@task()
def main():
    recommend_limit = 5
    recommendations = []
    user_data_df = prepare_data()
    x_axis, y_axis = get_x_y_axis(user_data_df)

    # naive_clf = apply_naive_bayes(x_axis, y_axis)
    # k_neighbours_clf = apply_k_neighbours(x_axis, y_axis)
    decision_tree_clf = apply_decision_tree(x_axis, y_axis)
    # adaboost_clf = apply_adaboost(x_axis, y_axis)

    recommendations = decision_tree_clf.predict(x_axis[:recommend_limit])



    rec_obj = RecommendedData()
    rec_obj.hotel_id = ",".join([str(val) for val in recommendations])
    rec_obj.save()

    print(recommendations)
