# ChatGPT 账号异常怎么办：陌生登录、凭证泄露、账号被停用、意外扣款

**最后核实：2026-09-29** · [← 返回总览](../README.md)

按你遇到的情况找对应的一节。所有情况的第一步都一样：**先把能收回的访问权收回，再慢慢查原因。**

## 目录

- [通用急救 5 步](#通用急救-5-步)
- [情况一：发现陌生登录或不认识的设备](#情况一发现陌生登录或不认识的设备)
- [情况二：把密码、验证码或 Session 给了别人](#情况二把密码验证码或-session-给了别人)
- [情况三：账号被停用或受到限制](#情况三账号被停用或受到限制)
- [情况四：出现意外的 API 用量](#情况四出现意外的-api-用量)
- [情况五：银行卡上出现不认识的扣款](#情况五银行卡上出现不认识的扣款)
- [联系 OpenAI 支持时准备什么](#联系-openai-支持时准备什么)
- [来源](#来源)

## 通用急救 5 步

1. **修改密码**（用邮箱密码登录的账号）。用 Google、Apple 或 Microsoft 登录的，修改对应账号的密码并检查它的安全设置。
2. **退出所有设备**：ChatGPT 设置 → 安全 → 退出所有设备。所有会话完全退出最多需要 30 分钟，你自己的设备也要重新登录。
3. **开启多因素认证（MFA）**：在同一页面开启，可选身份验证器 App、通行密钥等方式。
4. **检查账号内容**：设置、记忆、自定义指令、已连接的应用、共享链接，有没有被改动或新增。
5. **保存证据**：陌生设备的记录、时间、截图，之后联系支持时用得上。

## 情况一：发现陌生登录或不认识的设备

**先做**：通用急救 5 步。

**再查**：

- 最近有没有在别处提交过 Session，或者在不熟悉的网站用 ChatGPT 账号登录过；
- 登录邮箱本身是否安全：邮箱被别人控制，ChatGPT 账号迟早也会被拿走，所以邮箱也要改密码、开 MFA；
- 同一个密码有没有在别的网站用过，有的话一并修改。

**如果陌生设备是你刚用过的代充服务**：在订单确认完成之后退出所有设备即可，这是正常的收回步骤（见 [Session 是什么](what-is-session.md#用完之后怎么收回)）。

## 情况二：把密码、验证码或 Session 给了别人

| 交出去的 | 风险 | 立刻做 |
|---|---|---|
| 密码 | 对方可以随时登录、改设置 | 改密码 → 退出所有设备 → 开 MFA |
| 邮箱或短信验证码 | 对方可能已经用它完成登录或修改了设置 | 退出所有设备 → 改密码 → 检查登录邮箱和安全设置有没有被改 |
| MFA 验证码或恢复码 | 对方可以绕开你的第二重验证 | 退出所有设备 → 重新设置 MFA，生成新的恢复码 |
| Session | 失效前对方可以访问账号 | 退出所有设备（开通还在进行时，先确认订单状态） |
| OpenAI API Key | 对方可以用你的额度调用 API | 在 API 平台删除这个 Key，检查用量 |

登录邮箱或安全设置已经被改掉、你自己登不进去的，尽快联系 OpenAI 支持。

## 情况三：账号被停用或受到限制

- 先看 OpenAI 发到登录邮箱的通知，里面通常写了原因类别和申诉入口。
- 按通知里的方式申诉，写清楚账号邮箱、发生时间和你了解的情况；**不要**在申诉里编造经过。
- 重要的聊天记录，如果还能登录，先在设置里导出数据。
- 通过第三方开通会员的，要知道条款层面的风险（见 [Session 与条款](what-is-session.md#和-openai-使用条款的关系)）；第三方渠道无法替你申诉，也无法替 OpenAI 作出任何保证。

本仓库不提供任何规避限制或换号的方法。

## 情况四：出现意外的 API 用量

ChatGPT 会员和 OpenAI API 是两套独立计费的产品。如果在 API 平台看到自己没发起过的用量：

1. 删除所有可能泄露的 API Key，按需重新创建；
2. 检查用量明细的时间和模型，确认从什么时候开始异常；
3. 设置或调低用量上限；
4. 联系 OpenAI 支持说明情况。

## 情况五：银行卡上出现不认识的扣款

- 先核对是不是自己或家人的订阅（包括 App Store、Google Play 的订阅记录）；
- 确认不是后，联系发卡行；OpenAI 帮助中心《Report Fraudulent ChatGPT or API Credit Purchase Charges》说明了向 OpenAI 报告这类扣款的方式；
- 通过第三方渠道付款的，扣款记录在支付宝或你的银行卡上，收款方是第三方，处理入口是该第三方和支付平台，不是 OpenAI。

## 联系 OpenAI 支持时准备什么

- 账号邮箱和登录方式；
- 发生的时间（写明时区）和经过；
- 陌生设备、陌生扣款的截图（遮住卡号等无关信息）；
- 你已经做过的处理（改密码、退出所有设备等）。

**不要**在任何工单、邮件或聊天里提供密码或一次性验证码；OpenAI 帮助中心也提醒，不要把它们提供给任何人。

## 来源

- OpenAI：[How can I keep my OpenAI accounts secure?](https://help.openai.com/en/articles/8304786-how-can-i-keep-my-openai-accounts-secure)：怀疑账号被盗用时尽快联系支持。
- OpenAI：[Enabling or disabling multi-factor authentication (MFA)](https://help.openai.com/en/articles/7967234)：安全设置入口、退出所有设备最多需要 30 分钟、MFA 方式。
- OpenAI：[Managing active sessions in ChatGPT](https://help.openai.com/en/articles/20001257-managing-active-sessions-in-chatgpt)：查看并退出活跃会话。
- OpenAI：[How can I contact support?](https://help.openai.com/en/articles/6614161-how-can-i-contact-support)：联系支持的入口；不要提供密码或一次性验证码。
- OpenAI：[Report Fraudulent ChatGPT or API Credit Purchase Charges](https://help.openai.com/en/articles/7242625-report-fraudulent-chatgpt-or-api-credit-purchase-charges)：发现不认识的扣款时怎么报告。
- OpenAI：[How do I export my ChatGPT history and data?](https://help.openai.com/en/articles/7260999-how-do-i-export-my-chatgpt-history-and-data)：导出聊天记录和数据。
- OpenAI：[What is ChatGPT Plus?](https://help.openai.com/en/articles/6950777-what-is-chatgpt-plus)：API 用量不包含在会员内，单独计费。

核对日期和存档链接见 [SOURCES.md](../SOURCES.md)。
