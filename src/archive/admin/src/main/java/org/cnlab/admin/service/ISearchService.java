package org.cnlab.admin.service;

import org.cnlab.admin.model.SearchModel;
import org.cnlab.common.QueryModel;

import java.util.List;

/**
 * Created by LiuYingBo on 2015/2/1.
 */
public interface ISearchService {
    /**
     0* @param searchModel
     * @return
     */
    void save(SearchModel searchModel) throws Exception;

    void update(SearchModel searchModel) throws Exception;

    void delete(SearchModel searchModel) throws Exception;

    List<SearchModel> querySearchs(QueryModel queryModel);

    long queryAllSearchCounts();
}
