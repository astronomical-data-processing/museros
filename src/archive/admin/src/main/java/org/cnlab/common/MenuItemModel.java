package org.cnlab.common;

/**
 * Created by LiuYingBo on 2015/2/1.
 */
public class MenuItemModel {
    public String getId() {
        return id;
    }

    public void setId(String id) {
        this.id = id;
    }

    public String getUrl() {
        return url;
    }

    public void setUrl(String url) {
        this.url = url;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getIcon() {
        return icon;
    }

    public void setIcon(String icon) {
        this.icon = icon;
    }

    public MenuItemModel(String url, String name, String icon, String id, boolean toggle, boolean selected) {
        this.url = url;
        this.name = name;
        this.icon = icon;
        this.id = id;
        this.toggle = toggle;
        this.selected = selected;
    }

    public String url;
    public String name;
    public String icon;
    public String id;
    public boolean toggle;
    public boolean selected;

    public MenuItemModel(String url, String name, String icon, String id) {
        this.url = url;
        this.name = name;
        this.icon = icon;
        this.id = id;
    }
}
