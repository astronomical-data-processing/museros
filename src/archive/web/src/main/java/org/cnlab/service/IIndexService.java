package org.cnlab.service;


import org.cnlab.model.IndexPartsModel;

import java.util.List;

/**
 * Created by cnlab on 2015/1/24.
 */
public interface IIndexService {
    public List<IndexPartsModel> findAllIndexPartsInfo();
}
