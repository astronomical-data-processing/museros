package org.cnlab.admin.service;

import org.cnlab.admin.model.MovieModel;
import org.cnlab.common.QueryModel;

import java.util.List;

/**
 * Created by LiuYingBo on 2015/2/1.
 */
public interface IMovieService {
    /**
     0* @param movieModel
     * @return
     */
    void save(MovieModel movieModel) throws Exception;

    void update(MovieModel movieModel) throws Exception;

    void delete(MovieModel movieModel) throws Exception;

    List<MovieModel> queryMovies(QueryModel queryModel);

    long queryAllMovieCounts();
}
