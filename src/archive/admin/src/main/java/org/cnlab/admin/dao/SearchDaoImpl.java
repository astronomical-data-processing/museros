package org.cnlab.admin.dao;

import org.cnlab.admin.model.SearchModel;
import org.cnlab.common.dao.impl.BaseDaoImpl;
import org.springframework.stereotype.Repository;

/**
 * Created by cnlab on 2015/1/24.
 */
@Repository("searchDao")
public class SearchDaoImpl extends BaseDaoImpl<SearchModel> implements ISearchDao {

}
