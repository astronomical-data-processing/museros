package org.cnlab.admin.dao;

import org.cnlab.admin.model.MovieModel;
import org.cnlab.common.dao.impl.BaseDaoImpl;
import org.springframework.stereotype.Repository;

/**
 * Created by cnlab on 2015/1/24.
 */
@Repository("movieDao")
public class MovieDaoImpl extends BaseDaoImpl<MovieModel> implements IMovieDao {

}
