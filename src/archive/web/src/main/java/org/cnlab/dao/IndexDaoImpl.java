package org.cnlab.dao;

import org.cnlab.common.dao.impl.BaseDaoImpl;
import org.cnlab.model.IndexPartsModel;
import org.springframework.stereotype.Repository;

/**
 * Created by cnlab on 2015/1/24.
 */
@Repository("indexDao")
public class IndexDaoImpl extends BaseDaoImpl<IndexPartsModel> implements IIndexDao {

}
