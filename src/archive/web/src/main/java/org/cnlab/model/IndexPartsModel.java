package org.cnlab.model;

import java.util.List;

/**
 * 主页部件模型
 */
public class IndexPartsModel {
    private List<ImageModel> imageList;
    private List<MovieModel> movieList;
    private List<SolarEventModel> eventList;

    public List<SolarEventModel> getEventList() {
        return eventList;
    }

    public void setEventList(List<SolarEventModel> eventList) {
        this.eventList = eventList;
    }

    public List<ImageModel> getImageList() {
        return imageList;
    }

    public void setImageList(List<ImageModel> imageList) {
        this.imageList = imageList;
    }

    public List<MovieModel> getMovieList() {
        return movieList;
    }

    public void setMovieList(List<MovieModel> movieList) {
        this.movieList = movieList;
    }
}
