package org.cnlab.service;

import org.cnlab.model.SolarEventModel;
import org.cnlab.common.QueryModel;

import java.util.List;

/**
 * Created by LiuYingBo on 2015/2/1.
 */
public interface ISolarEventService {
    /**
     0* @param solarEventModel
     * @return
     */
    void save(SolarEventModel solarEventModel) throws Exception;

    void update(SolarEventModel solarEventModel) throws Exception;

    void delete(SolarEventModel solarEventModel) throws Exception;

    List<SolarEventModel> querySolarEvents(QueryModel queryModel);

    long queryAllSolarEventCounts();
}
