# 来源与核对记录

**最近一次核对：2026-09-29**

- 本仓库关于 OpenAI 规则的每一条说法，都能在下表的原文里找到。转述尽量简短，不翻译或粘贴整段原文；原文与本仓库不一致时，以原文为准，也欢迎开 Issue 提醒。
- **核对方式**：help.openai.com 和 openai.com 对自动抓取返回 403。表中“存档”一列是用来核对的 Wayback Machine 快照；标“浏览器”的，是 2026-09-29 用浏览器直接打开原文核对的。发布或复核前，维护者会再用浏览器打开一遍。
- OpenAI 帮助中心也有简体中文页面，把链接里的 `/en/` 换成 `/zh-hans-cn/` 即可；本仓库以英文原文为准。
- 写作上只用“OpenAI 帮助中心”“OpenAI 使用条款”这类具体名称。

## OpenAI 条款与帮助中心

| # | 来源 | 核对了什么 | 用在哪里 | 核对方式 |
|---|---|---|---|---|
| O1 | [Terms of Use](https://openai.com/policies/row-terms-of-use/) | 2026-01-01 生效版：不得共享账号凭证，不得让他人使用自己的账号；账号下的所有活动由持有人负责 | README 声明、[Session](docs/what-is-session.md)、[7 项核验](docs/pre-purchase-checklist.md)、[骗局](docs/scam-patterns.md) | 浏览器；[存档 2026-09-27](https://web.archive.org/web/20260927204534/https://openai.com/policies/row-terms-of-use/) |
| O2 | [About ChatGPT Pro tiers](https://help.openai.com/en/articles/9793128-about-chatgpt-pro-tiers) | 两个 Pro 档位核心功能相同，较低一档用量为 Plus 的 5 倍；升级立即生效、降级在续费时生效；不支持年付；自 2026-09-10 起用量最高的档位暂停新订阅和升级，已有订阅照常续订；禁止行为包括共享凭证、让他人使用账号、转售访问权 | README「Plus 还是 Pro 5 倍版」、[Session](docs/what-is-session.md) | [存档 2026-09-19](https://web.archive.org/web/20260919102801/https://help.openai.com/en/articles/9793128-about-chatgpt-pro-tiers)，并对比了 09-03、09-12 两个存档 |
| O3 | [OpenAI Account Sharing Policy](https://help.openai.com/en/articles/10471989-openai-account-sharing-policy) | 账号只供创建它的个人使用；共享登录凭证会暴露个人数据和付款信息；疑似被盗用时改密码并开启双重验证 | [7 项核验](docs/pre-purchase-checklist.md)、[骗局 3](docs/scam-patterns.md)、[Session](docs/what-is-session.md) | 浏览器；[存档 2026-04-06](https://web.archive.org/web/20260406073712/https://help.openai.com/en/articles/10471989-openai-account-sharing-policy/) |
| O4 | [ChatGPT Supported Countries](https://help.openai.com/en/articles/7947663-chatgpt-supported-countries) | 支持的国家和地区列表；在列表以外的地区访问或提供访问，可能导致账号被封禁或停用 | [7 项核验](docs/pre-purchase-checklist.md) | [存档 2026-09-28](https://web.archive.org/web/20260928061321/https://help.openai.com/en/articles/7947663-chatgpt-supported-countries) |
| O5 | [What is ChatGPT Plus?](https://help.openai.com/en/articles/6950777-what-is-chatgpt-plus) | API 用量不包含在会员内，单独计费；文末关于 Pro 更高档位暂停新订阅的说明 | README、[账号异常](docs/account-anomaly-recovery.md) | [存档 2026-09-25](https://web.archive.org/web/20260925110407/https://help.openai.com/en/articles/6950777-what-is-chatgpt-plus) |
| O6 | [Managing active sessions in ChatGPT](https://help.openai.com/en/articles/20001257-managing-active-sessions-in-chatgpt) | 在 设置 → 安全 → 活跃会话 中查看登录设备，可以退出单个或全部会话 | [Session](docs/what-is-session.md)、[账号异常](docs/account-anomaly-recovery.md) | 浏览器 |
| O7 | [Enabling or disabling multi-factor authentication (MFA)](https://help.openai.com/en/articles/7967234) | 安全设置入口；多因素认证方式；退出所有设备后，所有会话完全退出最多需要 30 分钟 | README「付款后自己验收」、[Session](docs/what-is-session.md)、[账号异常](docs/account-anomaly-recovery.md) | [存档 2026-06-07](https://web.archive.org/web/20260607104059/https://help.openai.com/en/articles/7967234) |
| O8 | [How can I keep my OpenAI accounts secure?](https://help.openai.com/en/articles/8304786-how-can-i-keep-my-openai-accounts-secure) | 怀疑账号被盗用时尽快联系 OpenAI 支持 | [账号异常](docs/account-anomaly-recovery.md) | [存档 2026-06-08](https://web.archive.org/web/20260608100925/https://help.openai.com/en/articles/8304786-how-can-i-keep-my-openai-accounts-secure) |
| O9 | [How can I contact support?](https://help.openai.com/en/articles/6614161-how-can-i-contact-support) | 联系支持的入口和需要准备的信息；不要提供密码或一次性验证码 | [骗局 2](docs/scam-patterns.md)、[账号异常](docs/account-anomaly-recovery.md) | 浏览器 |
| O10 | [Report Fraudulent ChatGPT or API Credit Purchase Charges](https://help.openai.com/en/articles/7242625-report-fraudulent-chatgpt-or-api-credit-purchase-charges) | 看到不认识的扣款先查发票，可能是家人使用；怀疑盗刷应立即联系银行 | [账号异常](docs/account-anomaly-recovery.md) | 浏览器 |
| O11 | [How do I export my ChatGPT history and data?](https://help.openai.com/en/articles/7260999-how-do-i-export-my-chatgpt-history-and-data) | 在设置里导出聊天记录和数据；导出前须能访问账号 | [账号异常](docs/account-anomaly-recovery.md) | [存档 2026-03-31](https://web.archive.org/web/20260331094141/https://help.openai.com/en/articles/7260999-how-do-i-export-my-chatgpt-history-and-data) |

## KAI · 开gptAI 自有规则（利益相关）

| # | 来源 | 核对了什么 | 用在哪里 | 核对日期 |
|---|---|---|---|---|
| K1 | KAI 服务条款与帮助页（kaigpt.ai） | 开通对象为用户自己的账号，可开 Plus 或 Pro 5 倍版；不交付共享号或成品号；人民币标价、支付宝扫码；常规订单时效；有条件的退款规则 | README「KAI 的业务口径」 | 2026-09-28 |
| K2 | KAI 隐私政策（kaigpt.ai/privacy） | 不索取密码和验证码；Session 只在 KAI 自有兑换页 kaigpt.pro 提交，加密短时保存、只用于对应订单、任务结束或凭证过期后清除 | README「KAI 的业务口径」 | 2026-09-28 |

KAI 的规则只代表 KAI 自己，不代表 OpenAI 政策。本仓库写到 KAI 的 Session 步骤时，一律同时写明：只在 KAI 自有兑换页 kaigpt.pro 提交，不要通过私聊、邮件或工单发给任何人（包括客服）。

## 本仓库不写的内容

- Session 的获取步骤、截图或脚本；
- 任何规避地区限制、更换地区或填写账单地址的方法；
- 各档位的具体价格和额度数值：变化快，以 OpenAI 页面和账号内显示为准；
- 没有出处的用户数、成功率、评价；
- 其他服务方的名称和价格。
