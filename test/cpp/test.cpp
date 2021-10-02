#include "test.h"

namespace abelkhan
{

/*this caller code is codegen by abelkhan codegen for cpp*/
std::shared_ptr<test_rsp_cb> test_caller::rsp_cb_test_handle = nullptr;
test_test3_cb::test_test3_cb(uint64_t _cb_uuid, std::shared_ptr<test_rsp_cb> _module_rsp_cb) {
    cb_uuid = _cb_uuid;
    module_rsp_cb = _module_rsp_cb;
}

std::shared_ptr<test_test3_cb> test_test3_cb::callBack(std::function<void(test1 t1, int32_t i)> cb, std::function<void(test1 err, std::vector<uint8_t> bytearray)> err) {
    sig_test3_cb.connect(cb);
    sig_test3_err.connect(err);
    return shared_from_this();
}

void test_test3_cb::timeout(uint64_t tick, std::function<void()> timeout_cb) {
    TinyTimer::add_timer(tick, [this](){
        module_rsp_cb->test3_timeout(cb_uuid);
    });
    sig_test3_timeout.connect(timeout_cb);
}


}
