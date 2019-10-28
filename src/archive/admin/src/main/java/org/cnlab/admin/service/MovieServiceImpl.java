package org.cnlab.admin.service;

import org.apache.log4j.Logger;
import org.cnlab.admin.model.MovieModel;
import org.cnlab.common.Constants;
import org.cnlab.common.QueryModel;
import org.springframework.stereotype.Service;

import javax.annotation.Resource;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

/**
 * Created by LiuYingBo on 2015/2/1.
 */
@Service("movieService")
public class MovieServiceImpl implements IMovieService {
    private static final Logger logger = Logger.getLogger(LoginServiceImpl.class);

    @Resource(name = "movieDao")
    private org.cnlab.admin.dao.IMovieDao movieDao;
    /**
     * 0* @param movieModel
     *
     * @param movieModel
     * @return
     */
    @Override
    public void save(MovieModel movieModel) throws Exception {
        try {
            movieDao.save(movieModel);
        } catch (Exception e) {
            logger.error("save error" + e.toString());
            throw e;
        }
    }

    @Override
    public void update(MovieModel movieModel) throws Exception {
        Map<String, Object> map = new HashMap<String, Object>();
        map.put("name", movieModel.getName());
        map.put("movieID", movieModel.getMovieID());
        try {
            movieDao.executeHQL("update MovieModel u set u.movieName=:movieName,u.name=:name,u.modifiedTime=:modifiedTime where u.movieID=:movieID",map);
        } catch (Exception e) {
            logger.error("save error" + e.toString());
            throw e;
        }
    }

    @Override
    public void delete(MovieModel movieModel) throws Exception {
        try {
            movieDao.delete(movieModel);
        } catch (Exception e) {
            logger.error("save error" + e.toString());
            throw e;
        }
    }

    @Override
    public List<MovieModel> queryMovies(QueryModel queryModel) {
        Map<String, Object> map = new HashMap<String, Object>();
        map.put("movieName", Constants.SUPERADMIN);
        return movieDao.find("from MovieModel u where u.movieName !=:movieName",map,queryModel.currentPage,queryModel.pageSize);
    }

    @Override
    public long queryAllMovieCounts() {
        return movieDao.count(" select count(*) from MovieModel");
    }
}
