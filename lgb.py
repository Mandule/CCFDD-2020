#!/usr/bin/env python
# coding: utf-8

# In[1]:


import gc
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
pd.set_option('display.max_columns', None)


# In[2]:


from lightgbm.sklearn import LGBMRegressor
from sklearn.model_selection import GroupKFold
from sklearn.metrics import f1_score


# In[3]:


import warnings
from tqdm import tqdm
tqdm.pandas(desc='pandas bar')
warnings.filterwarnings('ignore')


# In[15]:


def f1_score_eval(y_true, y_pred):
    scores = f1_score(y_true=y_true, y_pred=y_pred, average=None)
    scores = scores[0]*0.2+scores[1]*0.2+scores[2]*0.6
    return scores


# In[25]:


def search_f1(label, oof, sub):
    best = 0
    best_t0 = 0.0
    best_t1 = 0.0
    t0 = oof.min()
    step = 0.01
    while t0 < 1.0:
        pred0 = (oof<t0).astype(int)
        t1 = t0+step
        while t1 < 3.0:
            pred1 = ((oof>t0)&(oof<t1)).astype(int)*2
            pred3 = (oof>t1).astype(int)*3
            pred = pred0 + pred1 + pred3
            score = f1_score_eval(label, pred)
            if score > best:
                best = score
                best_t0 = t0
                best_t1 = t1
            t1+=step
        t0+=step
    
    print('best_f1_score: {} | best_threshold: {}'.format(best, [best_t0, best_t1]))
    pred_sub = (sub<best_t0).astype(int) + ((sub>best_t0)&(sub<best_t1)).astype(int)*2 + (sub>best_t1).astype(int)*3
    return pred_sub


# In[4]:


traffic = pd.read_pickle('data/traffic.pkl')
traffic.head()


# In[5]:


attr = pd.read_csv('data/attr.csv')
attr.head()


# In[6]:


traffic = traffic[traffic.date.isin([26,27,28,29,30,31])].reset_index(drop=True)
traffic = traffic.merge(attr, how='left', on='link_id')
traffic['time_diff'] = traffic.pred_time - traffic.cur_time


# In[7]:


df_train = traffic[traffic.label>0].reset_index(drop=True)
df_test = traffic[traffic.label<0].reset_index(drop=True)


# In[8]:


del traffic
del attr
gc.collect()


# In[9]:


feats = df_train.columns.drop(['date', 'label'])
category_feats = ['link_id', 'direction']


# In[10]:


class_weight = dict(df_train.shape[0] / (3 * df_train.label.value_counts()))
df_train['weight'] = df_train.label.map(class_weight)


# In[11]:


oof = np.zeros(df_train.shape[0])
sub = np.zeros(df_test.shape[0])
feat_imp_df = pd.DataFrame({'feat': feats, 'imp': 0.0})
gkf = GroupKFold(n_splits=5)


# In[12]:


print('train shape {} test shape {}'.format(df_train.shape, df_test.shape))


# In[13]:


for i, (trn_idx, val_idx) in enumerate(gkf.split(df_train, groups=(df_train.date.map(str) + '_' + df_train.link_id.map(str)))):
    print('------------------------------{} fold------------------------------'.format(i))
    X_trn, Y_trn, W_trn = df_train.iloc[trn_idx][feats], df_train.iloc[trn_idx].label, df_train.iloc[trn_idx].weight
    X_val, Y_val, W_val = df_train.iloc[val_idx][feats], df_train.iloc[val_idx].label, df_train.iloc[val_idx].weight
    X_sub = df_test[feats]
    
    clf = LGBMRegressor(
        num_leaves=63,
        learning_rate=0.02,
        n_estimators=100000,
        subsample=0.6,
        colsample_bytree=0.6,
        random_state=2020,
        n_jobs=24,
    )
    
    clf.fit(
        X_trn, Y_trn,
        sample_weight= W_trn,
        eval_set=[(X_val, Y_val)],
        eval_metric='rmse',
        eval_sample_weight=[W_val],
        early_stopping_rounds=200,
        categorical_feature=category_feats,
        verbose=100,
    )
    
    oof[val_idx] = clf.predict(X_val)
    sub +=  clf.predict(X_sub) / gkf.n_splits
    feat_imp_df['imp'] += clf.feature_importances_ / gkf.n_splits


# In[ ]:

pred_sub = search_f1(df_train.label, oof, sub)

# In[ ]:

plt.figure(figsize=(15, 30))
feat_imp_df = feat_imp_df.sort_values('imp', ignore_index=True)
sns.barplot(x='imp', y='feat', data=feat_imp_df)
plt.savefig('imp.png')

# In[ ]:

pd.DataFrame({
    'link': df_test.link_id,
    'current_slice_id': df_test.cur_time,
    'future_slice_id': df_test.pred_time,
    'label': pred_sub,
}).to_csv('sub.csv', index=False)

