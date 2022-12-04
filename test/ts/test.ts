import * as abelkhan from "./abelkhan";
/*this enum code is codegen by abelkhan codegen for ts*/

export enum em_test3{
    enum_test3 = 1,
    enum_test1 = 2,
    enum_test2 = 3
}

/*this struct code is codegen by abelkhan codegen for typescript*/
export class test1
{
    public argv1 : number;
    public argv2 : string = "123";
    public argv3 : number;
    public argv4 : number;

    constructor(){
    }
}

export function test1_to_protcol(_struct:test1){
    return _struct;
}

export function protcol_to_test1(_protocol:any){
    let _struct = new test1();
    for (const [key, val] of Object.entries(_protocol))        if (key === "argv1"){
            _struct.argv1 = val as number;
        }
        else if (key === "argv2"){
            _struct.argv2 = val as string;
        }
        else if (key === "argv3"){
            _struct.argv3 = val as number;
        }
        else if (key === "argv4"){
            _struct.argv4 = val as number;
        }
    return _struct;
}

export class test2
{
    public argv1 : number = 0;
    public argv2 : test1;
    public bytel : Uint8Array = Uint8Array.from([1,1,9]);
    public t : em_test3 = em_test3.enum_test3;

    constructor(){
    }
}

export function test2_to_protcol(_struct:test2){
    return _struct;
}

export function protcol_to_test2(_protocol:any){
    let _struct = new test2();
    for (const [key, val] of Object.entries(_protocol))        if (key === "argv1"){
            _struct.argv1 = val as number;
        }
        else if (key === "argv2"){
            _struct.argv2 = protcol_to_test1(val);
        }
        else if (key === "bytel"){
            _struct.bytel = val as Uint8Array;
        }
        else if (key === "t"){
            _struct.t = val as em_test3;
        }
    return _struct;
}

export class test3
{
    public em : em_test3 = em_test3.enum_test3;
    public em_list : em_test3[];

    constructor(){
    }
}

export function test3_to_protcol(_struct:test3){
    return _struct;
}

export function protcol_to_test3(_protocol:any){
    let _struct = new test3();
    for (const [key, val] of Object.entries(_protocol))        if (key === "em"){
            _struct.em = val as em_test3;
        }
        else if (key === "em_list"){
            _struct.em_list = [];
            for(let v_ of val){
                _struct.em_list.push(v_);
    }
        }
    return _struct;
}

/*this caller code is codegen by abelkhan codegen for typescript*/
export class test_test3_cb{
    private cb_uuid : number;
    private module_rsp_cb : test_rsp_cb;

    public event_test3_handle_cb : (t1:test1, i:number)=>void | null;
    public event_test3_handle_err : (err:test1, bytearray:Uint8Array)=>void | null;
    public event_test3_handle_timeout : ()=>void | null;
    constructor(_cb_uuid : number, _module_rsp_cb : test_rsp_cb){
        this.cb_uuid = _cb_uuid;
        this.module_rsp_cb = _module_rsp_cb;
        this.event_test3_handle_cb = null;
        this.event_test3_handle_err = null;
        this.event_test3_handle_timeout = null;
    }

    callBack(_cb:(t1:test1, i:number)=>void, _err:(err:test1, bytearray:Uint8Array)=>void)
    {
        this.event_test3_handle_cb = _cb;
        this.event_test3_handle_err = _err;
        return this;
    }

    timeout(tick:number, timeout_cb:()=>void)
    {
        setTimeout(()=>{ this.module_rsp_cb.test3_timeout(this.cb_uuid); }, tick);
        this.event_test3_handle_timeout = timeout_cb;
    }

}

/*this cb code is codegen by abelkhan for ts*/
export class test_rsp_cb extends abelkhan.Imodule {
    public map_test3:Map<number, test_test3_cb>;
    constructor(modules:abelkhan.modulemng){
        super("test_rsp_cb");
        this.map_test3 = new Map<number, test_test3_cb>();
        modules.reg_method("test_rsp_cb_test3_rsp", [this, this.test3_rsp.bind(this)]);
        modules.reg_method("test_rsp_cb_test3_err", [this, this.test3_err.bind(this)]);
    }
    public test3_rsp(inArray:any[]){
        let uuid = inArray[0];
        let _argv_bf7f1e5a_6b28_310c_8f9e_f815dbd56fb7:any[] = [];
        _argv_bf7f1e5a_6b28_310c_8f9e_f815dbd56fb7.push(protcol_to_test1(inArray[1]));
        _argv_bf7f1e5a_6b28_310c_8f9e_f815dbd56fb7.push(inArray[2]);
        var rsp = this.try_get_and_del_test3_cb(uuid);
        if (rsp && rsp.event_test3_handle_cb) {
            rsp.event_test3_handle_cb.apply(null, _argv_bf7f1e5a_6b28_310c_8f9e_f815dbd56fb7);
        }
    }

    public test3_err(inArray:any[]){
        let uuid = inArray[0];
        let _argv_bf7f1e5a_6b28_310c_8f9e_f815dbd56fb7:any[] = [];
        _argv_bf7f1e5a_6b28_310c_8f9e_f815dbd56fb7.push(protcol_to_test1(inArray[1]));
        _argv_bf7f1e5a_6b28_310c_8f9e_f815dbd56fb7.push(inArray[2]);
        var rsp = this.try_get_and_del_test3_cb(uuid);
        if (rsp && rsp.event_test3_handle_err) {
            rsp.event_test3_handle_err.apply(null, _argv_bf7f1e5a_6b28_310c_8f9e_f815dbd56fb7);
        }
    }

    public test3_timeout(cb_uuid : number){
        let rsp = this.try_get_and_del_test3_cb(cb_uuid);
        if (rsp){
            if (rsp.event_test3_handle_timeout) {
                rsp.event_test3_handle_timeout.apply(null);
            }
        }
    }

    private try_get_and_del_test3_cb(uuid : number){
        var rsp = this.map_test3.get(uuid);
        this.map_test3.delete(uuid);
        return rsp;
    }

}

export let rsp_cb_test_handle : test_rsp_cb | null = null;
export class test_caller extends abelkhan.Icaller {
    private uuid_45a113ac_c7f2_30b0_90a5_a399ab912716 : number = Math.round(Math.random() * 1000);

    constructor(_ch:any, modules:abelkhan.modulemng){
        super("test", _ch);
        if (rsp_cb_test_handle == null){
            rsp_cb_test_handle = new test_rsp_cb(modules);
        }
    }

    public test3(t2:test2, e:em_test3 = em_test3.enum_test3, str:string = "qianqians"){
        let uuid_20ca53af_d04c_58a2_a8b3_d02b9e414e80 = Math.round(this.uuid_45a113ac_c7f2_30b0_90a5_a399ab912716++);

        let _argv_bf7f1e5a_6b28_310c_8f9e_f815dbd56fb7:any[] = [uuid_20ca53af_d04c_58a2_a8b3_d02b9e414e80];
        _argv_bf7f1e5a_6b28_310c_8f9e_f815dbd56fb7.push(test2_to_protcol(t2));
        _argv_bf7f1e5a_6b28_310c_8f9e_f815dbd56fb7.push(e);
        _argv_bf7f1e5a_6b28_310c_8f9e_f815dbd56fb7.push(str);
        this.call_module_method("test_test3", _argv_bf7f1e5a_6b28_310c_8f9e_f815dbd56fb7);

        let cb_test3_obj = new test_test3_cb(uuid_20ca53af_d04c_58a2_a8b3_d02b9e414e80, rsp_cb_test_handle);
        if (rsp_cb_test_handle){
            rsp_cb_test_handle.map_test3.set(uuid_20ca53af_d04c_58a2_a8b3_d02b9e414e80, cb_test3_obj);
        }
        return cb_test3_obj;
    }

    public test4(argv:test2[], num:number = 0.110){
        let _argv_fe584e24_96c8_3d2d_8b39_f1cc6a877f72:any[] = [];
        let _array_80252816_2442_30bc_bd5c_59666cae8a23:any[] = [];
        for(let v_51e4d59a_5357_5634_9bc1_e9c2e0aa9ab0 of argv){
            _array_80252816_2442_30bc_bd5c_59666cae8a23.push(test2_to_protcol(v_51e4d59a_5357_5634_9bc1_e9c2e0aa9ab0));
        }
        _argv_fe584e24_96c8_3d2d_8b39_f1cc6a877f72.push(_array_80252816_2442_30bc_bd5c_59666cae8a23);
        _argv_fe584e24_96c8_3d2d_8b39_f1cc6a877f72.push(num);
        this.call_module_method("test_test4", _argv_fe584e24_96c8_3d2d_8b39_f1cc6a877f72);
    }

}
/*this module code is codegen by abelkhan codegen for typescript*/
export class test_test3_rsp extends abelkhan.Icaller {
    private uuid_77eeaa2a_8150_3cce_bfa0_0b16e18637bd : number;
    constructor(_ch:abelkhan.Ichannel, _uuid:number){
        super("test_rsp_cb", _ch);
        this.uuid_77eeaa2a_8150_3cce_bfa0_0b16e18637bd = _uuid;
    }

    public rsp(t1:test1, i:number = 110){
        let _argv_bf7f1e5a_6b28_310c_8f9e_f815dbd56fb7:any[] = [this.uuid_77eeaa2a_8150_3cce_bfa0_0b16e18637bd];
        _argv_bf7f1e5a_6b28_310c_8f9e_f815dbd56fb7.push(test1_to_protcol(t1));
        _argv_bf7f1e5a_6b28_310c_8f9e_f815dbd56fb7.push(i);
        this.call_module_method("test_rsp_cb_test3_rsp", _argv_bf7f1e5a_6b28_310c_8f9e_f815dbd56fb7);
    }

    public err(err:test1, bytearray:Uint8Array = Uint8Array.from([1,1,0])){
        let _argv_bf7f1e5a_6b28_310c_8f9e_f815dbd56fb7:any[] = [this.uuid_77eeaa2a_8150_3cce_bfa0_0b16e18637bd];
        _argv_bf7f1e5a_6b28_310c_8f9e_f815dbd56fb7.push(test1_to_protcol(err));
        _argv_bf7f1e5a_6b28_310c_8f9e_f815dbd56fb7.push(bytearray);
        this.call_module_method("test_rsp_cb_test3_err", _argv_bf7f1e5a_6b28_310c_8f9e_f815dbd56fb7);
    }

}

export class test_module extends abelkhan.Imodule {
    private modules:abelkhan.modulemng;
    constructor(modules:abelkhan.modulemng){
        super("test");
        this.modules = modules;
        this.modules.reg_method("test_test3", [this, this.test3.bind(this)]);
        this.modules.reg_method("test_test4", [this, this.test4.bind(this)]);

        this.cb_test3 = null;
        this.cb_test4 = null;
    }

    public cb_test3 : (t2:test2, e:em_test3, str:string)=>void | null;
    test3(inArray:any[]){
        let _cb_uuid = inArray[0];
        let _argv_:any[] = [];
        _argv_.push(protcol_to_test2(inArray[1]));
        _argv_.push(inArray[2]);
        _argv_.push(inArray[3]);
        this.rsp = new test_test3_rsp(this.current_ch, _cb_uuid);
        if (this.cb_test3){
            this.cb_test3.apply(null, _argv_);
        }
        this.rsp = null;
    }

    public cb_test4 : (argv:test2[], num:number)=>void | null;
    test4(inArray:any[]){
        let _argv_:any[] = [];
        let _array_:any[] = [];
        for(let v_ of inArray[0]){
            _array_.push(protcol_to_test2(v_));
        }
        _argv_.push(_array_);
        _argv_.push(inArray[1]);
        if (this.cb_test4){
            this.cb_test4.apply(null, _argv_);
        }
    }

}
