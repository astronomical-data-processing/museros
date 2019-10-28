package org.cnlab.admin.model;

import javax.persistence.*;
import java.sql.Timestamp;

/**
 * Created by cnlab on 2015/1/24.
 * 全部用大写
 */
@Entity
@Table(name = "T_SolarEvent")
public class SolarEventModel {
    //事件ID
    private int SolarEventID;
    private long EventID;
    private Timestamp EventDate;
    private String Peak;
    private String Duratn;
    private String COR;
    private String Brightness;
    private String F17G;
    private String F34G;
    private float AreaRatio;
    private String Position;
    private float X;
    private float Y;
    private String Implulse;
    private String GOES;
    private String NOAA;
    private String Keyword;
    private String RHESSI;
    private String Energy;

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "SolarEventID")
    public int getSolarEventID() {
        return SolarEventID;
    }

    public void setSolarEventID(int solarEventID) {
        SolarEventID = solarEventID;
    }

    @Column(name = "AreaRatio")
    public float getAreaRatio() {
        return AreaRatio;
    }

    public void setAreaRatio(float areaRatio) {
        AreaRatio = areaRatio;
    }

    @Column(name = "Brightness")
    public String getBrightness() {
        return Brightness;
    }

    public void setBrightness(String brightness) {
        Brightness = brightness;
    }

    @Column(name = "COR")
    public String getCOR() {
        return COR;
    }

    public void setCOR(String COR) {
        this.COR = COR;
    }

    @Column(name = "Duratn")
    public String getDuratn() {
        return Duratn;
    }

    public void setDuratn(String duratn) {
        Duratn = duratn;
    }

    @Column(name = "Energy")
    public String getEnergy() {
        return Energy;
    }

    public void setEnergy(String energy) {
        Energy = energy;
    }

    @Column(name = "EventDate")
    public Timestamp getEventDate() {
        return EventDate;
    }

    public void setEventDate(Timestamp eventDate) {
        EventDate = eventDate;
    }

    @Column(name = "EventID")
    public long getEventID() {
        return EventID;
    }

    public void setEventID(long eventID) {
        EventID = eventID;
    }

    @Column(name = "F17G")
    public String getF17G() {
        return F17G;
    }

    public void setF17G(String f17G) {
        F17G = f17G;
    }

    @Column(name = "F34G")
    public String getF34G() {
        return F34G;
    }

    public void setF34G(String f34G) {
        F34G = f34G;
    }

    @Column(name = "GOES")
    public String getGOES() {
        return GOES;
    }

    public void setGOES(String GOES) {
        this.GOES = GOES;
    }

    @Column(name = "Implulse")
    public String getImplulse() {
        return Implulse;
    }

    public void setImplulse(String implulse) {
        Implulse = implulse;
    }

    @Column(name = "Keyword")
    public String getKeyword() {
        return Keyword;
    }

    public void setKeyword(String keyword) {
        Keyword = keyword;
    }

    @Column(name = "NOAA")
    public String getNOAA() {
        return NOAA;
    }

    public void setNOAA(String NOAA) {
        this.NOAA = NOAA;
    }

    @Column(name = "Peak")
    public String getPeak() {
        return Peak;
    }

    public void setPeak(String peak) {
        Peak = peak;
    }

    @Column(name = "Position")
    public String getPosition() {
        return Position;
    }

    public void setPosition(String position) {
        Position = position;
    }

    @Column(name = "RHESSI")
    public String getRHESSI() {
        return RHESSI;
    }

    public void setRHESSI(String RHESSI) {
        this.RHESSI = RHESSI;
    }

    @Column(name = "X")
    public float getX() {
        return X;
    }

    public void setX(float x) {
        X = x;
    }

    @Column(name = "Y")
    public float getY() {
        return Y;
    }

    public void setY(float y) {
        Y = y;
    }

}
