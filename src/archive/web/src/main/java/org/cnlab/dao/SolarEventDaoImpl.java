package org.cnlab.dao;

import org.cnlab.model.SolarEventModel;
import org.cnlab.common.dao.impl.BaseDaoImpl;
import org.springframework.stereotype.Repository;

/**
 * Created by cnlab on 2015/1/24.
 */
@Repository("solarEventDao")
public class SolarEventDaoImpl extends BaseDaoImpl<SolarEventModel> implements ISolarEventDao {

}
