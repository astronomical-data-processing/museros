package org.cnlab.admin.model;

import javax.persistence.*;
import java.sql.Timestamp;

/**
 * Created by cnlab on 2015/1/24.
 */
@Entity
@Table(name = "T_Event")
public class EventModel {
    //事件ID
    private int EventID;
    //事件名
    private String EventName;
    //登录账号
    private String UserName;
    //IP
    private String IP;
    //操作
    private String Operation;
    //时间发生日期
    private Timestamp EventDateTime;

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "EventID")
    public int getEventID() {
        return EventID;
    }

    public void setEventID(int eventID) {
        EventID = eventID;
    }

    @Column(name = "EventName", length = 100)
    public String getEventName() {
        return EventName;
    }

    public void setEventName(String eventName) {
        EventName = eventName;
    }

    @Column(name = "UserName", length = 20)
    public String getUserName() {
        return UserName;
    }

    public void setUserName(String userName) {
        UserName = userName;
    }

    @Column(name = "IP", length = 20)
    public String getIP() {
        return IP;
    }

    public void setIP(String IP) {
        this.IP = IP;
    }

    @Column(name = "Operation", length = 20)
    public String getOperation() {
        return Operation;
    }

    public void setOperation(String operation) {
        Operation = operation;
    }

    @Column(name = "EventDateTime", length = 20)
    public Timestamp getEventDateTime() {
        return EventDateTime;
    }

    public void setEventDateTime(Timestamp eventDateTime) {
        EventDateTime = eventDateTime;
    }


}
